package com.example.dsi_ppai.repositories;

import com.example.dsi_ppai.models.rol;

import java.util.List;
import java.util.stream.Stream;

public class rolRepo extends Repository<rol, Long>{
    public rolRepo(){super();}

    @Override
    public List<rol> getAll() {
        return this.manager.createQuery("SELECT r FROM rol r", rol.class)
                .getResultList();
    }


    @Override
    public Stream<rol> getAllStream() {
        return this.manager.createQuery("SELECT r FROM rol r", rol.class)
                .getResultStream();
    }

    @Override
    public rol getById(Long id) {
        return this.manager.find(rol.class, id);
    }
}

