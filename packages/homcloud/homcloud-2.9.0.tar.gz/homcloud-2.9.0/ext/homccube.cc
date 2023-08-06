#pragma GCC diagnostic ignored "-Wunused-function"
#include "homcloud_common.h"

#include "homccube/basic_types.hpp"
#include "homccube/bitmap.hpp"
#include "homccube/link_find.hpp"
#include "homccube/reduce.hpp"
#include "homccube/config.hpp"
#include "homccube/cube.hpp"
#include "homccube/dipha_format.hpp"
#include "homccube/dipha.hpp"

#include <memory>
#include <sstream>

using homccube::Bitmap;
using homccube::BasicTypes;
using homccube::Cube;
using homccube::Config;

static std::vector<int> ShapeFromArray(PyArrayObject* array) {
  npy_intp* shape = PyArray_DIMS(array);
  return std::vector<int>(shape, shape + PyArray_NDIM(array));
}
    
static bool IsValidShape(const std::vector<int>& shape) {
  if (shape.size() == 2) {
    if (BasicTypes<2>::valid_shape(shape)) {
      return true;
    } else {
      PyErr_SetString(PyExc_ValueError,
                      "Invalid shape: array must be smaller than 32766x32766");
      return false;
    }
  }
  if (shape.size() == 3) {
    if (BasicTypes<3>::valid_shape(shape)) {
      return true;
    } else {
      PyErr_SetString(PyExc_ValueError,
                      "Invalid shape: array must be smaller than 2046x2046x1022 "
                      "and number of voxels <= 536870908");
      return false;
    }
  }

  PyErr_SetString(PyExc_ValueError, "HomcCube supports only 2D and 3D bitmaps");
  return false;
}

template<int maxdim>
PyObject* DiphaDegree(int degree, typename BasicTypes<maxdim>::PixelLevel death) {
  static const auto INFINITE_LEVEL = BasicTypes<maxdim>::INFINITE_LEVEL;
  return PyLong_FromLong((death == INFINITE_LEVEL) ? -1 - degree : degree);
}

template<int maxdim, int dim>
using Survivors = std::shared_ptr<std::vector<Cube<maxdim, dim>>>;

template<int maxdim>
Survivors<maxdim, 1>
Compute0thPD(const Bitmap<maxdim>& bitmap,
               PyObject* degrees, PyObject* births, PyObject* deaths) {
  PyObject* degree = nullptr;
  PyObject* birth = nullptr;
  PyObject* death = nullptr;
  homccube::LinkFind<maxdim> link_find(bitmap);
  link_find.compute();

  size_t num_pairs = link_find.birth_levels_.size();
  for (size_t i = 0; i < num_pairs; ++i) {
    degree = DiphaDegree<maxdim>(0, link_find.death_levels_[i]);
    if (!degree) goto error;
    if (PyList_Append(degrees, degree) < 0) goto error;
    Py_CLEAR(degree);

    birth = PyLong_FromLong(link_find.birth_levels_[i]);
    if (!birth) goto error;
    if (PyList_Append(births, birth) < 0) goto error;
    Py_CLEAR(birth);

    death = PyLong_FromLong(link_find.death_levels_[i]);
    if (!death) goto error;
    if (PyList_Append(deaths, death) < 0) goto error;
    Py_CLEAR(death);
  }

  return link_find.survivors_;

error:
  Py_XDECREF(degree);
  Py_XDECREF(birth);
  Py_XDECREF(death);
  return nullptr;
}

template<int maxdim, int dim>
Survivors<maxdim, dim + 1>
ComputeKthPD(const Bitmap<maxdim>& bitmap,
             const Survivors<maxdim, dim> lower_survivors, Config config,
             PyObject* degrees, PyObject* births, PyObject* deaths) {
  PyObject* degree = nullptr;
  PyObject* birth = nullptr;
  PyObject* death = nullptr;
  if (maxdim < dim || (maxdim == dim && lower_survivors->size() == 0))
    return std::make_shared<std::vector<homccube::Cube<maxdim, dim + 1>>>();

  homccube::Reducer<maxdim, dim> reducer(bitmap, lower_survivors, config);
  reducer.compute();

  size_t num_pairs = reducer.birth_levels_.size();
  for (size_t i = 0; i < num_pairs; ++i) {
    degree = DiphaDegree<maxdim>(dim, reducer.death_levels_[i]);
    if (!degree) goto error;
    if (PyList_Append(degrees, degree) < 0) goto error;
    Py_CLEAR(degree);

    birth = PyLong_FromLong(reducer.birth_levels_[i]);
    if (!birth) goto error;
    if (PyList_Append(births, birth) < 0) goto error;
    Py_CLEAR(birth);

    death = PyLong_FromLong(reducer.death_levels_[i]);
    if (!death) goto error;
    if (PyList_Append(deaths, death) < 0) goto error;
    Py_CLEAR(death);
  }

  return reducer.upper_survivors();

error:
  Py_XDECREF(degree);
  Py_XDECREF(birth);
  Py_XDECREF(death);
  return nullptr;
}

template<int maxdim>
typename BasicTypes<maxdim>::Period
ParsePeriodicityList(PyObject* periodicity) {
  typename BasicTypes<maxdim>::Period p(0);
  for (int i = 0; i < maxdim; ++i)
    p[i] = PyObject_IsTrue(PyList_GetItem(periodicity, i));
  return p;
}

template<int maxdim>
void LoadLevels(PyArrayObject* array, Bitmap<maxdim>* bitmap) {
  npy_int32* data = reinterpret_cast<npy_int32*>(PyArray_DATA(array));
  std::copy(data, data + bitmap->num_vertices_, bitmap->levels_.begin());
}

template<int maxdim>
void Run(PyArrayObject* array, PyObject* periodicity,
         const std::vector<int>& shape, Config config,
         PyObject* degrees, PyObject* births, PyObject* deaths) {
  Bitmap<maxdim> bitmap(shape, ParsePeriodicityList<maxdim>(periodicity), false);
  LoadLevels(array, &bitmap);

  auto survivors0 = Compute0thPD(bitmap, degrees, births, deaths);
  auto survivors1 = ComputeKthPD(bitmap, survivors0, config, degrees, births, deaths);
  auto survivors2 = ComputeKthPD(bitmap, survivors1, config, degrees, births, deaths);
  ComputeKthPD(bitmap, survivors2, config, degrees, births, deaths);
}

template<int maxdim>
void Run(PyArrayObject* array, PyObject* periodicity,
         const std::vector<int>& shape, Config config, std::ostream* out) {
  using namespace homccube::dipha;
  Bitmap<maxdim> bitmap(shape, ParsePeriodicityList<maxdim>(periodicity), false);
  LoadLevels(array, &bitmap);

  skip_diagram_header(out);
  uint64_t num_pairs = 0;
  auto survivors0 = compute_0th_pd(bitmap, out, &num_pairs);
  auto survivors1 = compute_kth_pd(bitmap, survivors0, config, out, &num_pairs);
  auto survivors2 = compute_kth_pd(bitmap, survivors1, config, out, &num_pairs);
  auto survivors3 = compute_kth_pd(bitmap, survivors2, config, out, &num_pairs);
    
  out->seekp(0, std::ios_base::beg);
  write_diagram_header(num_pairs, out);
}

static PyObject* compute_pd(PyObject* self, PyObject* args) {
  using homccube::CacheStrategy;
  using homccube::strategy_from_string;

  PyObject* ary;
  PyObject* periodicity;
  char* algorithm;
  int dipha_format;
  
  Config config;

  PyArrayObject* array = nullptr;
  PyObject* degrees = nullptr;
  PyObject* births = nullptr;
  PyObject* deaths = nullptr;

  if (!PyArg_ParseTuple(args, "OO!sp", &ary, &PyList_Type, &periodicity, &algorithm,
                        &dipha_format))
    return nullptr;

  array = reinterpret_cast<PyArrayObject*>(PyArray_FROM_OTF(ary, NPY_INT32, NPY_ARRAY_C_CONTIGUOUS));
  if (!array) return nullptr;

  int ndim = PyArray_NDIM(array);

  if (PyList_Size(periodicity) != ndim) {
    PyErr_SetString(PyExc_ValueError, "Periodicity list length mismatch");
    return nullptr;
  }

  std::vector<int> shape = ShapeFromArray(array);
  
  if (!IsValidShape(shape))
    return nullptr;

  config.cache_strategy_ = strategy_from_string(algorithm);
  if (config.cache_strategy_ == CacheStrategy::UNKNOWN) {
    PyErr_Format(PyExc_ValueError, "Unknown cache strategy: %s", algorithm);
    return nullptr;
  }

  if (dipha_format) {
    std::ostringstream out;

    if (ndim == 2) Run<2>(array, periodicity, shape, config, &out);
    if (ndim == 3) Run<3>(array, periodicity, shape, config, &out);
    
    Py_DECREF(array);
    return Py_BuildValue("y#", out.str().data(), out.str().size());
  } else {
    degrees = PyList_New(0); if (!degrees) goto error;
    births = PyList_New(0); if (!births) goto error;
    deaths = PyList_New(0); if (!deaths) goto error;

    if (ndim == 2) Run<2>(array, periodicity, shape, config, degrees, births, deaths);
    if (ndim == 3) Run<3>(array, periodicity, shape, config, degrees, births, deaths);
  
    Py_DECREF(array);
    return Py_BuildValue("(OOO)", degrees, births, deaths);
  }

error:
  Py_XDECREF(array);
  Py_XDECREF(degrees);
  Py_XDECREF(births);
  Py_XDECREF(deaths);
  return nullptr;
}

static PyMethodDef homccube_Methods[] = {
  {"compute_pd", (PyCFunction)compute_pd, METH_VARARGS,
   "Compute a persistence diagram from bitmap"},
  {NULL, NULL, 0, NULL},
};

static PyModuleDef homccube_Module = {
  PyModuleDef_HEAD_INIT,
  "homcloud.homccube",
  "The module for homccube",
  -1,
  homccube_Methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit_homccube()
{
  PyObject* module = PyModule_Create(&homccube_Module);
  if (!module)
    return nullptr;

  import_array();

  return module;
}
