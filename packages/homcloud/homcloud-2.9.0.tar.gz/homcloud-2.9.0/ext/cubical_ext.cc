#include "homcloud_common.h"
#include <cstdint>
#include <cmath>
#include <vector>
#include <unordered_map>
#include <limits>
#include <iostream>
#include <bitset>
#include <sstream>
#include <algorithm>

#define HOMCLOUD_PHAT_EXT_MODULE
#include "phat_ext.h"

using CubeID = unsigned long long;

struct StringWriter {
  std::string* buf_;

  StringWriter(std::string* buf) {
    buf_ = buf;
  }

  template<typename T>
  void Write(T n) {
    buf_->append(reinterpret_cast<char*>(&n), sizeof(T));
  }
};

struct CubicalFiltrationExt {
  PyObject_HEAD
  PyArrayObject* array_;
  PyObject* periodic_;
  int ndim_;
  npy_intp* shape_;
  std::vector<npy_intp>* required_bits_;
  std::vector<npy_intp>* bottom_bit_;
  std::vector<double>* cache_value_at_;
  std::vector<CubeID>* sorted_cubes_;
  CubeID cubedim_mask_;
  bool indexized_;
  bool save_boundary_map_;

  static npy_intp RequiredBits1D(npy_intp n) {
    for (npy_intp k = 0; k < 32; ++k)
      if ((1 << k) >= n)
        return k + 1;
    return -1;
  }

  CubeID BuildCubeDimMask() {
    CubeID mask = 0;
    for (int k = 0; k < ndim_; ++k)
      mask |= 1 << (bottom_bit_->at(k));
    return mask;
  }

  void SetUp(PyArrayObject* array, PyObject* periodic, bool save_boundary_map) {
    ndim_ = PyArray_NDIM(array);
    shape_ = PyArray_DIMS(array);
    array_ = array;
    periodic_ = periodic;
    Py_INCREF(array_);
    Py_INCREF(periodic_);

    required_bits_ = new std::vector<npy_intp>(ndim_);
    bottom_bit_ = new std::vector<npy_intp>(ndim_ + 1);

    bottom_bit_->at(0) = 0;
    for (int n = 0; n < ndim_; ++n) {
      npy_intp bits = RequiredBits1D(shape_[n]);
      required_bits_->at(n) = bits;
      bottom_bit_->at(n + 1) = bottom_bit_->at(n) + bits;
    }

    cache_value_at_ = new std::vector<double>(1 << bottom_bit_->at(ndim_),
                                             std::numeric_limits<double>::quiet_NaN());

    cubedim_mask_ = BuildCubeDimMask();
    indexized_ = false;
    save_boundary_map_ = save_boundary_map;
  }

  void TearDown() {
    Py_XDECREF(array_);
    Py_XDECREF(periodic_);
    delete required_bits_; required_bits_ = nullptr;
    delete bottom_bit_; bottom_bit_ = nullptr;
    delete cache_value_at_; cache_value_at_ = nullptr;
    delete sorted_cubes_; sorted_cubes_ = nullptr;
  }

  CubeID Mask(int n) {
    return ((1 << required_bits_->at(n)) - 1);
  }

  CubeID Encode(const std::vector<npy_intp>& coords,
                const std::vector<npy_intp>& non_degenerate) const {
    CubeID id = 0;
    for (int n = ndim_ - 1; n >= 0; --n) {
      id = (id << required_bits_->at(n)) | (coords[n] << 1) | non_degenerate[n];
    }
    return id;
  }

  void Decode(CubeID id,
              std::vector<npy_intp>* coords,
              std::vector<npy_intp>* non_degenerate) {
    for (int n = 0; n < ndim_; ++n) {
      CubeID slice = id & Mask(n);
      coords->at(n) = slice >> 1;
      non_degenerate->at(n) = slice & 1;
      id >>= required_bits_->at(n);
    }
  }

  int CubeDim(CubeID id) {
#ifdef __GNUC__
    return __builtin_popcountll(id & cubedim_mask_);
#else
    int dim = 0;
    for (int n = 0; n < ndim_; ++n) {
      dim += (id & Mask(n)) & 1;
      id >>= required_bits_->at(n);
    }
    return dim;
#endif
  }

  CubeID BuildFacet(CubeID partial, CubeID coface, CubeID mask, int n) {
    return (coface & ~mask) | (partial << (bottom_bit_->at(n) + 1));
  }

  std::vector<CubeID> Facets(CubeID id) {
    std::vector<CubeID> result;

    for (int n = 0; n < ndim_; ++n) {
      CubeID mask = Mask(n) << bottom_bit_->at(n);
      CubeID slice = (id & mask) >> bottom_bit_->at(n);
      if (slice & 1) {
        result.push_back(BuildFacet(((slice >> 1) + 1) % shape_[n], id, mask, n));
        result.push_back(BuildFacet(slice >> 1, id, mask, n));
      }
    }
    return result;
  }

  std::vector<int> BoundarySigns(CubeID id) {
    int dim = CubeDim(id);
    std::vector<int> result(2 * dim);
    for (int i = 0; i < 2 * dim; ++i) 
      result[i] = (i % 4 == 0 || i % 4 == 3) ? 1 : -1;
    return result;
  }

  double ValueAt(CubeID id) {
    double cache_value = cache_value_at_->at(id);
    if (!std::isnan(cache_value))
      return cache_value;
    
    double value;
    if (CubeDim(id) == 0) {
      std::vector<npy_intp> coords(ndim_);
      std::vector<npy_intp> non_degenerate(ndim_);
      Decode(id, &coords, &non_degenerate);
      value = *reinterpret_cast<double*>(PyArray_GetPtr(array_, coords.data()));
    } else {
      auto facets = Facets(id);
      value = std::max(ValueAt(facets[0]), ValueAt(facets[1]));
    }
    
    cache_value_at_->at(id) = value;

    return value;
  }

  bool ValidCoords(const std::vector<npy_intp>& coords,
                   const std::vector<npy_intp>& non_degenerate) const {
    for (int n = 0; n < ndim_; ++n) {
      if (PyObject_IsTrue(PySequence_GetItem(periodic_, n)))
        continue;
      if (coords[n] + non_degenerate[n] >= shape_[n])
        return false;
    }
    return true;
  }

  void AllCubesIter(int n,
                    std::vector<npy_intp>* indexlist,
                    std::vector<npy_intp>* non_degenerate,
                    std::vector<CubeID>* result) {
    if (n == ndim_) {
      CubeID cubeid = Encode(*indexlist, *non_degenerate);
      if (ValidCoords(*indexlist, *non_degenerate) && ValueAt(cubeid) != INFINITY) {
        result->push_back(cubeid);
      }
      return;
    }

    for (npy_intp k = 0; k < shape_[n]; ++k) {
      indexlist->at(n) = k;
      for (npy_intp nd=0; nd <= 1; ++nd) {
        non_degenerate->at(n) = nd;
        AllCubesIter(n + 1, indexlist, non_degenerate, result);
      }
    }
  }
                    
  std::vector<CubeID> AllCubes() {
    std::vector<CubeID> result;
    std::vector<npy_intp> indexlist(ndim_);
    std::vector<npy_intp> non_degenerate(ndim_);
    
    AllCubesIter(0, &indexlist, &non_degenerate, &result);
    return result;
  }

  bool CompareCube(CubeID x, CubeID y) {
    double x_value = ValueAt(x);
    double y_value = ValueAt(y);
    if (x_value != y_value)
      return x_value < y_value;
    else
      return CubeDim(x) < CubeDim(y);
  }

  void PrepareSortedCubes() {
    if (sorted_cubes_)
      return;

    sorted_cubes_ = new std::vector<CubeID>();
    *sorted_cubes_ = std::move(AllCubes());
    std::stable_sort(sorted_cubes_->begin(), sorted_cubes_->end(),
                     [this](CubeID x, CubeID y) { return CompareCube(x, y); });
  }

  std::vector<int64_t> Cube2Index() {
    std::vector<int64_t> cube2index(1 << bottom_bit_->at(ndim_));
    for (unsigned n = 0; n < sorted_cubes_->size(); ++n)
      cube2index[(*sorted_cubes_)[n]] = n;
    return cube2index;
  }

  std::string DiphaByteSequence() {
    std::string buf;
    StringWriter output(&buf);

    PrepareSortedCubes();
    std::vector<int64_t> cube2index = Cube2Index();

    // Write headers
    output.Write<int64_t>(8067171840);
    output.Write<int64_t>(0);
    output.Write<int64_t>(0);
    output.Write<int64_t>(sorted_cubes_->size());
    output.Write<int64_t>(ndim_);
    
    // Write dimensions
    for (CubeID cube : *sorted_cubes_)
      output.Write<int64_t>(CubeDim(cube));

    // Write birth time
    if (indexized_) {
      for (unsigned i = 0; i < sorted_cubes_->size(); ++i)
        output.Write<double>(i);
    } else {
      for (CubeID cube : *sorted_cubes_)
        output.Write<double>(ValueAt(cube));
    }

    // Write Boundary map sizes
    int n = 0;
    for (CubeID cube : *sorted_cubes_) {
      output.Write<int64_t>(n);
      n += CubeDim(cube) * 2;
    }
    output.Write<int64_t>(n);

    // Write boundary map
    for (CubeID cube : *sorted_cubes_)
      for (CubeID facet : Facets(cube))
        output.Write<int64_t>(cube2index[facet]);

    return buf;
  }

  phat_ext::Matrix* BuildPhatMatrix() {
    PrepareSortedCubes();
    phat_ext::Matrix* matrix = phat_ext::MatrixNew(
        sorted_cubes_->size(), save_boundary_map_ ? "cubical" : "none");
        
    if (!matrix) return nullptr;

    auto cube2index = Cube2Index();

    for (unsigned i = 0; i < sorted_cubes_->size(); ++i) {
      CubeID cube = sorted_cubes_->at(i);
      std::vector<CubeID> facets = Facets(cube);
      std::vector<phat::index> facet_ids(facets.size());
      std::transform(facets.begin(), facets.end(), facet_ids.begin(),
                     [&cube2index](CubeID id) { return cube2index[id]; });
      matrix->SetDimCol(i, CubeDim(cube), &facet_ids);
    }
    
    return matrix;
  }
}; // struct CubicalFiltrationExt

namespace CubicalFiltrationExt_methods {

static void dealloc(CubicalFiltrationExt* self) {
  self->TearDown();
  Py_TYPE(self)->tp_free(cast_PyObj(self));
}

static int init(CubicalFiltrationExt* self, PyObject* args, PyObject* kwds) {
  PyArrayObject* array;
  PyObject* periodic;
  int save_boundary_map;
  
  if (!PyArg_ParseTuple(args, "O!O!p", &PyArray_Type, &array,
                        &PyList_Type, &periodic, &save_boundary_map))
    return -1;

  if (!ArrayIsDoubleType(array))
    return -1;

  self->SetUp(array, periodic, save_boundary_map);

  return 0;
}

static bool ValidSequence(PyObject* obj, int expected_size) {
  return PySequence_Check(obj) && (PySequence_Size(obj) == expected_size);
}

static PyObject* get_required_bits(PyObject* self_, void* closure) {
  CubicalFiltrationExt* self = reinterpret_cast<CubicalFiltrationExt*>(self_);
  PyObject* list = PyList_New(self->ndim_);

  if (!list)
    return nullptr;

  for (int n = 0; n < self->ndim_; ++n) {
    PyObject* bits = PyLong_FromLong(self->required_bits_->at(n));
    if (!bits)
      goto error;

    PyList_SET_ITEM(list, n, bits);
  }
  return list;

error:
  Py_XDECREF(list);
  return nullptr;
}

static PyObject* get_sorted_cubes(CubicalFiltrationExt* self, void* closure) {
  self->PrepareSortedCubes();
  PyObject* list = PyList_New(self->sorted_cubes_->size());
  
  if (!list)
    return nullptr;

  for (unsigned n = 0; n < self->sorted_cubes_->size(); ++n) {
    PyObject* cube = PyLong_FromLong((*self->sorted_cubes_)[n]);
    if (!cube) goto error;
    PyList_SET_ITEM(list, n, cube);
  }

  return list;
error:
  Py_XDECREF(list);
  return nullptr;
}

static PyObject* encode_cube(CubicalFiltrationExt* self, PyObject* args) {
  PyObject* coords;
  PyObject* non_degenerate;

  if (!PyArg_ParseTuple(args, "OO", &coords, &non_degenerate))
    return nullptr;

  if (!ValidSequence(coords, self->ndim_) ||
      !ValidSequence(non_degenerate, self->ndim_)) {
    PyErr_SetString(PyExc_RuntimeError,
                    "coords or non_degenerate is not a valid sequence");
    return nullptr;
  }

  std::vector<npy_intp> v_coords(self->ndim_);
  std::vector<npy_intp> v_non_degenerate(self->ndim_);
  for (int n = 0; n < self->ndim_; ++n) {
    v_coords[n] = PyLong_AsLong(PySequence_GetItem(coords, n));
    v_non_degenerate[n] = PyLong_AsLong(PySequence_GetItem(non_degenerate, n));
  }
  return PyLong_FromLong(self->Encode(v_coords, v_non_degenerate));
}

static PyObject* decode_cube(CubicalFiltrationExt* self, PyObject* args) {
  CubeID id;
  if (!PyArg_ParseTuple(args, "K", &id))
    return nullptr;

  std::vector<npy_intp> v_coords(self->ndim_);
  std::vector<npy_intp> v_non_degenerate(self->ndim_);

  self->Decode(id, &v_coords, &v_non_degenerate);

  PyObject* coords = nullptr;
  PyObject* non_degenerate = nullptr;

  coords = PyList_New(self->ndim_);
  non_degenerate = PyList_New(self->ndim_);
  if (!coords || !non_degenerate)
    goto error;

  for (int n = 0; n < self->ndim_; ++n) {
    PyObject* coord = PyLong_FromLong(v_coords[n]);
    if (!coord) goto error;
    PyList_SET_ITEM(coords, n, coord);
    
    PyObject* ndeg = PyLong_FromLong(v_non_degenerate[n]);
    if (!ndeg) goto error;
    PyList_SET_ITEM(non_degenerate, n, ndeg);
  }

  return Py_BuildValue("(OO)", coords, non_degenerate);

error:
  Py_XDECREF(coords);
  Py_XDECREF(non_degenerate);
  return nullptr;
}

PyObject* cube_dim(CubicalFiltrationExt* self, PyObject* args) {
  CubeID id;
  if (!PyArg_ParseTuple(args, "K", &id))
    return nullptr;

  return PyLong_FromLong(self->CubeDim(id));
}

PyObject* boundary(CubicalFiltrationExt* self, PyObject* args) {
  CubeID id;
  if (!PyArg_ParseTuple(args, "K", &id))
    return nullptr;

  int cube_dim = self->CubeDim(id);
    
  std::vector<CubeID> facets = self->Facets(id);
  std::vector<int> signs = self->BoundarySigns(id);
  PyObject* facets_list = PyList_New(cube_dim * 2);
  if (!facets_list)
    return nullptr;
  
  PyObject* signs_list = PyList_New(cube_dim * 2);
  if (!signs_list) {
    Py_XDECREF(facets_list);
    return nullptr;
  }

  for (int i = 0; i < 2 * cube_dim; ++i) {
    PyList_SET_ITEM(facets_list, i, PyLong_FromLong(facets[i]));
    PyList_SET_ITEM(signs_list, i, PyLong_FromLong(signs[i]));
  }

  return Py_BuildValue("(OO)", facets_list, signs_list);
}

PyObject* value_at(CubicalFiltrationExt* self, PyObject* args) {
  CubeID id;
  if (!PyArg_ParseTuple(args, "K", &id))
    return nullptr;

  return PyFloat_FromDouble(self->ValueAt(id));
}

PyObject* all_cubes(CubicalFiltrationExt* self) {
  PyObject* list = PyList_New(0);
  PyObject* cubeint = nullptr;

  auto all_cubes = self->AllCubes();
  for (CubeID cube : all_cubes) {
    cubeint = PyLong_FromLong(cube);
    if (!cubeint) goto error;
    if (PyList_Append(list, cubeint) < 0)
      goto error;
  }

  return list;
error:
  Py_XDECREF(list);
  Py_XDECREF(cubeint);
  return nullptr;
}

PyObject* dipha_byte_sequence(CubicalFiltrationExt* self) {
  std::string buf = self->DiphaByteSequence();
  return PyBytes_FromStringAndSize(buf.c_str(), buf.size());
}

PyObject* indexize_internal(CubicalFiltrationExt* self) {
  if (self->indexized_)
    Py_RETURN_NONE;

  self->PrepareSortedCubes();

  npy_intp dims[]= {static_cast<npy_intp>(self->sorted_cubes_->size())};
  PyObject* levels = PyArray_SimpleNew(1, dims, NPY_DOUBLE);

  if (!levels)
    return nullptr;

  for (unsigned i = 0; i < self->sorted_cubes_->size(); ++i)
    *GETPTR1D<double>((PyArrayObject*)levels, i) = self->ValueAt((*self->sorted_cubes_)[i]);

  self->indexized_ = true;

  return levels;
}

static PyObject* build_phat_matrix(CubicalFiltrationExt* self) {
  phat_ext::Matrix* matrix = self->BuildPhatMatrix();
  if (!matrix) {
    PyErr_SetString(PyExc_RuntimeError, "Build phat matrix error");
    return nullptr;
  }
    
  return reinterpret_cast<PyObject*>(matrix);
}

static PyMethodDef methods[] = {
  {"encode_cube", (PyCFunction)encode_cube, METH_VARARGS, "Encode cube id"},
  {"decode_cube", (PyCFunction)decode_cube, METH_VARARGS, "Decode cube id"},
  {"cube_dim", (PyCFunction)cube_dim, METH_VARARGS, "Dimension of the cube id"},
  {"boundary", (PyCFunction)boundary, METH_VARARGS, "Boundary map"},
  {"value_at", (PyCFunction)value_at, METH_VARARGS, "Level of the cube"},
  {"all_cubes", (PyCFunction)all_cubes, METH_NOARGS, "List of all cubes"},
  {"dipha_byte_sequence", (PyCFunction)dipha_byte_sequence, METH_NOARGS,
   "Byte sequence for dipha"},
  {"indexize_internal", (PyCFunction)indexize_internal, METH_NOARGS,
   "Indexize internally"},
  {"build_phat_matrix", (PyCFunction)build_phat_matrix, METH_NOARGS,
   "Return phat' matrix object"},
  {NULL}
};

static PyMemberDef members[] = {
  {"array", T_OBJECT, offsetof(CubicalFiltrationExt, array_), READONLY,
   "Numpy array object"},
  {NULL}
};

static PyGetSetDef getsetters[] = {
  {"required_bits", get_required_bits, nullptr,
   "Required bits for each coordinate"},
  {"sorted_cubes", (getter)get_sorted_cubes, nullptr, "Sorted cubes"},
  {NULL}
};

} // namespace CubicalFiltrationExt_methods

static PyTypeObject CubicalFiltrationExtType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "homcloud.cubical_ext.CubicalFiltrationExt", // tp_name
  sizeof(CubicalFiltrationExt), // tp_basicsize
  0, // tp_itemsize
  (destructor)CubicalFiltrationExt_methods::dealloc, // tp_dealloc
  0, // tp_print
  0, // tp_getattr
  0, // tp_setattr
  0, // tp_reserved
  0, // tp_repr
  0, // tp_as_number
  0, // tp_as_sequence
  0, // tp_as_mapping
  0, // tp_hash 
  0, // tp_call
  0, // tp_str
  0, // tp_getattro
  0, // tp_setattro
  0, // tp_as_buffer
  Py_TPFLAGS_DEFAULT|Py_TPFLAGS_BASETYPE, // tp_flags 
  "Class for fast cubical filtration",  // tp_doc 
  0, // tp_traverse
  0, // tp_clear
  0, // tp_richcompare
  0, // tp_weaklistoffset
  0, // tp_iter
  0, // tp_iternext
  CubicalFiltrationExt_methods::methods,  // tp_methods 
  CubicalFiltrationExt_methods::members, // tp_members
  CubicalFiltrationExt_methods::getsetters, // tp_getset
  0, // tp_base
  0, // tp_dict
  0, // tp_descr_get
  0, // tp_descr_set
  0, // tp_dictoffset
  reinterpret_cast<initproc>(CubicalFiltrationExt_methods::init), // tp_init
  0, // tp_alloc
  PyType_GenericNew, // tp_new
}; 

static PyModuleDef cubical_ext_Module = {
  PyModuleDef_HEAD_INIT,
  "homcloud.cubical_ext",
  "The module for fast cubical filtrations",
  -1,
  NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit_cubical_ext()
{
  if (PyType_Ready(&CubicalFiltrationExtType) < 0)
    return nullptr;

  PyObject* module = PyModule_Create(&cubical_ext_Module);
  if (!module)
    return nullptr;

  Py_INCREF(&CubicalFiltrationExtType);
  PyModule_AddObject(module, "CubicalFiltrationExt",
                     cast_PyObj(&CubicalFiltrationExtType));

  import_array();
  phat_ext::import();

  return module;
}
