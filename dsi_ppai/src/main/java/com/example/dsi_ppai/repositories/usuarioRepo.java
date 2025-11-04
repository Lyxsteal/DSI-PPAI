package com.example.dsi_ppai.repositories;

import com.example.dsi_ppai.models.usuario;

import java.util.List;
import java.util.stream.Stream;

public class usuarioRepo extends Repository<usuario, Long>{
    public usuarioRepo(){super();}

    @Override
    public List<usuario> getAll() {
        return this.manager.createQuery("SELECT u FROM usuario u", usuario.class)
                .getResultList();
    }


    @Override
    public Stream<usuario> getAllStream() {
        return this.manager.createQuery("SELECT u FROM usuario u", usuario.class)
                .getResultStream();
    }

    @Override
    public usuario getById(Long id) {
        return this.manager.find(usuario.class, id);
    }
}


