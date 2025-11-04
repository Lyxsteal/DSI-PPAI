package com.example.dsi_ppai.repositories;


import com.example.dsi_ppai.models.sismografo;

import java.util.List;
import java.util.stream.Stream;

public class sismografoRepo extends Repository<sismografo, Long>{
    public sismografoRepo(){super();}

    @Override
    public List<sismografo> getAll() {
        return this.manager.createQuery("SELECT si FROM sismografo si", sismografo.class)
                .getResultList();
    }


    @Override
    public Stream<sismografo> getAllStream() {
        return this.manager.createQuery("SELECT si FROM sismografo si", sismografo.class)
                .getResultStream();
    }

    @Override
    public sismografo getById(Long id) {
        return this.manager.find(sismografo.class, id);
    }
}

