package edu.usta.interfaces;

import java.util.List;

public interface Funcionalidad<T> {
    public Boolean registrar(T elObjeto);
    public List<T> consultar(String orden);
    T buscar(Integer llavePrimaria);
    Boolean eliminar(Integer llavePrimaria);
    Boolean actualizar(T elObjeto);
    Integer totalRegistros();
}