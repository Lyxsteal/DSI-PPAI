package com.example.dsi_ppai.repositories;

import com.example.dsi_ppai.models.estacionSismo;

import java.util.List;
import java.util.stream.Stream;

public class estacionSismoRepo extends Repository<estacionSismo, Long>{
    public estacionSismoRepo(){super();}

    @Override
    public List<estacionSismo> getAll() {
        return this.manager.createQuery("SELECT es FROM estacionSismo es", estacionSismo.class)
                .getResultList();
    }


    @Override
    public Stream<estacionSismo> getAllStream() {
        return this.manager.createQuery("SELECT es FROM estacionSismo es", estacionSismo.class)
                .getResultStream();
    }

    @Override
    public estacionSismo getById(Long id) {
        return this.manager.find(estacionSismo.class, id);
    }
}


