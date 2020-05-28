package fr.newexplorers;

import java.util.List;

public class Blob {
    private int _nbKernels;
    private Kernel _kernel;

    public Blob() {
        _kernel = new Kernel();
    }

    public Blob(Blob blob, int nbKernels) {
        _kernel = blob.copyKernel();
        _nbKernels = nbKernels;
    }

    private Kernel copyKernel() {
        // TODO: copy Kernel
        return new Kernel();
    }

    public Blob Cut(int nb) {
        return new Blob(this, nb);
    }
}