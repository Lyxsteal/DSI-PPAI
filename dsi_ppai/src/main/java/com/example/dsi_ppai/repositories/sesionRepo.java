package com.example.dsi_ppai.repositories;

import com.example.dsi_ppai.models.sesion;

import java.util.List;
import java.util.stream.Stream;

public class sesionRepo extends Repository<sesion, Long>{
    public sesionRepo(){super();}

    @Override
    public List<sesion> getAll() {
        return this.manager.createQuery("SELECT s FROM sesion s", sesion.class)
                .getResultList();
    }


    @Override
    public Stream<sesion> getAllStream() {
        return this.manager.createQuery("SELECT s FROM sesion s", sesion.class)
                .getResultStream();
    }

    @Override
    public sesion getById(Long id) {
        return this.manager.find(sesion.class, id);
    }
}

