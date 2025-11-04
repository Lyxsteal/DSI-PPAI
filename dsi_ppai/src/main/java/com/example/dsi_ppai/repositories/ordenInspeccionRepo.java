package com.example.dsi_ppai.repositories;

import com.example.dsi_ppai.models.ordenInspeccion;

import java.util.List;
import java.util.stream.Stream;

public class ordenInspeccionRepo extends Repository<ordenInspeccion, Long>{
    public ordenInspeccionRepo(){super();}

    @Override
    public List<ordenInspeccion> getAll() {
        return this.manager.createQuery("SELECT oi FROM ordenInspeccion oi", ordenInspeccion.class)
                .getResultList();
    }


    @Override
    public Stream<ordenInspeccion> getAllStream() {
        return this.manager.createQuery("SELECT oi FROM ordenInspeccion oi", ordenInspeccion.class)
                .getResultStream();
    }

    @Override
    public ordenInspeccion getById(Long id) {
        return this.manager.find(ordenInspeccion.class, id);
    }
}


