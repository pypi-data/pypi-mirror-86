import argparse
import sys

import numpy as np

import homcloud.utils as utils
from homcloud.version import __version__
from homcloud.diagram import PD


def main(args=None):
    args = args or argument_parser().parse_args()
    diagrams = [PD.load(args.type, path, args.degree) for path in args.input]
    pwgk = PWGK(args, diagrams)
    kernels = pwgk.compute_gram_matrix()
    if args.output:
        np.savetxt(args.output, kernels)
    else:
        np.savetxt(sys.stdout.buffer, kernels)


def argument_parser():
    p = argparse.ArgumentParser(description="Create a gram matrix from diagrams")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-d", "--degree", type=int, required=True, help="degree of PH")
    p.add_argument("-T", "--type",
                   help="input file format (dipha, idipha, text) (default: autodetect)")
    utils.add_arguments_for_gaussian_diffusion(p)
    utils.add_arguments_for_kernel_weight(p)
    p.add_argument("-s", "--second-gaussian-sd", type=float, help="second gaussian parameter")
    p.add_argument("-N", "--num-samples", type=int, default=1000,
                   help="number of samples for computing PWGK with Monte-Carlo")
    p.add_argument("-o", "--output", help="output file")
    p.add_argument("input", nargs="+", help="input files(diagrams)")
    return p


class PWGK(object):
    def __init__(self, args, diagrams):
        self.weight_c = args.C
        self.weight_p = args.p
        self.sigma = args.gaussian_sd
        self.tau = args.second_gaussian_sd
        self.num_samples = args.num_samples
        self.diagrams = diagrams
        self.num_diagrams = len(diagrams)

    def compute_blobs(self):
        """Compute intermediate data.

        The name of blog means nothing. Please give us a good name.
        """
        def weight(diagram):
            return np.arctan(self.weight_c*(diagram.deaths - diagram.births)**self.weight_p)

        def blob(diagram, b_omega, d_omega):
            return np.sum(weight(diagram)*
                          np.exp(1j*(b_omega*diagram.births + d_omega*diagram.deaths)))

        b_omegas = np.random.normal(scale=1/self.sigma, size=self.num_samples)
        d_omegas = np.random.normal(scale=1/self.sigma, size=self.num_samples)

        blobs = np.empty((len(self.diagrams), self.num_samples), dtype=complex)
        for (i, diagram) in enumerate(self.diagrams):
            for (j, (b_omega, d_omega)) in enumerate(zip(b_omegas, d_omegas)):
                blobs[i, j] = blob(diagram, b_omega, d_omega)

        return blobs

    def compute_logkernels(self):
        blobs = self.compute_blobs()
        k = np.inner(blobs, np.conj(blobs))
        logkernels = np.empty((self.num_diagrams, self.num_diagrams), dtype=complex)

        for i in range(self.num_diagrams):
            for j in range(self.num_diagrams):
                logkernels[i, j] = (k[i, i] + k[j, j] - 2*k[i, j])/self.num_samples

        return logkernels

    def compute_gram_matrix(self):
        logkernels = self.compute_logkernels()
        return np.exp(-np.real(logkernels)/(2*self.tau**2))


if __name__ == "__main__":
    main()
