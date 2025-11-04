package com.example.dsi_ppai.repositories;
import com.example.dsi_ppai.models.motivosFueraServicio;

import java.util.List;
import java.util.stream.Stream;

public class motivosFueraServicioRepo extends Repository<motivosFueraServicio, Long>{
    public motivosFueraServicioRepo(){super();}

    @Override
    public List<motivosFueraServicio> getAll() {
        return this.manager.createQuery("SELECT mfs FROM motivosFueraServicio mfs", motivosFueraServicio.class)
                .getResultList();
    }


    @Override
    public Stream<motivosFueraServicio> getAllStream() {
        return this.manager.createQuery("SELECT mfs FROM motivosFueraServicio mfs", motivosFueraServicio.class)
                .getResultStream();
    }

    @Override
    public motivosFueraServicio getById(Long id) {
        return this.manager.find(motivosFueraServicio.class, id);
    }
}

