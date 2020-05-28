package fr.newexplorers;

public class Environment {
    private int _height;
    private int _width;

    public Environment(int height, int width) {
        _height = height;
        _width = width;
    }

    public int getHeight() {
        return _height;
    }

    public void setHeight(int height) {
        _height = height;
    }
}