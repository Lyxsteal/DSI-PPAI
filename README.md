# DSI-PPAI
Repositorio para PPAI de DSI

# Detalles
!! DS = Diagrama de Secuencia
- En pantallaOrdenInspeccion no deberia existir habilitar_segunda_pantalla() asi que la puse en habilitarPantalla()

- Elimine y mude pantallasOpciones para que tenga funcionalidad el metodo seleccionOpcionCerrarOrdenInspeccion() en la clase pantallaOrdenInspeccion pero agregue un metodo que no existe en DS llamado ayudaseleccionOpcionCerrarOrdenInspeccion() espero que no importe jejox

- Elimine y mude iniciarSesion() y obtenerUsuario() de gestor a pantalla porque en gestor no existen esos metodos en el DS

- Agruegue los nombres de los metodos que deberian ir en pantallaOrdenInspeccion

- Veran nosotros creamos el gestor en obtener_datos() de pantalla antes de la creacion de pantallaOrdenInspeccion es creada pero figura en el DS que la pantalla se crea antes del gestor y de hecho es la misma pantalla es la que lo crea (RESUELTO ahora el gestor se crea en pantalla en habilitarPantalla())

!! En un futuro ver si se cumple: 'habilita actualizar la situación del sismógrafo de la ES para ponerlo como Fuera de Servicio.'

- Modifique las relaciones con otras clases en el creador del gestor (comente los de antes por si pongo mal las cosas)

- Cree las clases que faltaban

- Agregue los nombres de los metodos que deberian ir en el gestor

-  Hice el primer loop, ahora salen las ordenes de inspeccion correspondientes para ser seleccionadas
