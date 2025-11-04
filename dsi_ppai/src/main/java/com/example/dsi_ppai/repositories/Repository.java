package com.example.dsi_ppai.repositories;

import jakarta.persistence.EntityManager;

import javax.swing.text.html.parser.Entity;
import java.util.List;
import java.util.stream.Stream;

public abstract class Repository<T, K> {
    protected EntityManager manager;
    public Repository(){manager = DbContext.getInstance().getManager();}

    public void add(T entity){
        var transaction = manager.getTransaction();
        transaction.begin();
        manager.persist(entity);
        transaction.commit();
    }
    public void update(T entity){
        var transaction = manager.getTransaction();
        transaction.begin();
        manager.merge(entity);
        transaction.commit();
    }
    public T delete(T entity){
        var transaction = manager.getTransaction();
        transaction.begin();
        manager.remove(entity);
        transaction.commit();
        return entity;
    }

    public abstract List<T> getAll();
    public abstract T getById(K id);
    public abstract Stream<T> getAllStream();
}
