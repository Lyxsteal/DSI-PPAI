package com.example.dsi_ppai.repositories;
import com.example.dsi_ppai.models.cambioEstado;

import java.util.List;
import java.util.stream.Stream;

public class cambioEstadoRepo extends Repository<cambioEstado, Long>{
    public cambioEstadoRepo(){super();}

    @Override
    public List<cambioEstado> getAll() {
        return this.manager.createQuery("SELECT ce FROM cambioEstado ce", cambioEstado.class)
                .getResultList();
    }


    @Override
    public Stream<cambioEstado> getAllStream() {
        return this.manager.createQuery("SELECT ce FROM cambioEstado ce", cambioEstado.class)
                .getResultStream();
    }

    @Override
    public cambioEstado getById(Long id) {
        return this.manager.find(cambioEstado.class, id);
    }
}

