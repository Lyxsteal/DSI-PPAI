package com.example.dsi_ppai.repositories;

import com.example.dsi_ppai.models.estado;

import java.util.List;
import java.util.stream.Stream;

public class estadoRepo extends Repository<estado, Long>{
    public estadoRepo(){super();}

    @Override
    public List<estado> getAll() {
        return this.manager.createQuery("SELECT e FROM estado e", estado.class)
                .getResultList();
    }


    @Override
    public Stream<estado> getAllStream() {
        return this.manager.createQuery("SELECT e FROM estado e", estado.class)
                .getResultStream();
    }

    @Override
    public estado getById(Long id) {
        return this.manager.find(estado.class, id);
    }
}


