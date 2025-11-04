package com.example.dsi_ppai.repositories;
import com.example.dsi_ppai.models.empleado;

import java.util.List;
import java.util.stream.Stream;

public class empleadoRepo extends Repository<empleado, Long>{
    public empleadoRepo(){super();}

    @Override
    public List<empleado> getAll() {
        return this.manager.createQuery("SELECT e FROM Empleado e", empleado.class)
                .getResultList();
    }


    @Override
    public Stream<empleado> getAllStream() {
        return this.manager.createQuery("SELECT e FROM Empleado e", empleado.class)
                .getResultStream();
    }

    @Override
    public empleado getById(Long id) {
        return this.manager.find(empleado.class, id);
    }
}

