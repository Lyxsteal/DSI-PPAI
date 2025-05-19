const host = "http://localhost:3000"

function creacionLocales(ordenes) {
    const table = document.getElementById("tbodyOrdenes");
   /*  table.innerHTML = ""; */
    ordenes.forEach((orden) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${orden.numeroOrden}</td>
            <td>${orden.fechaHoraFinalizacion}</td>
            <td>${orden.Nombre}</td>
            <td>${orden.estacion}</td>
            <td>${local.sismografo}</td>
        `;
        const contenido = row.innerHTML;
        console.log(contenido);
        table.appendChild(row);
    })};
async function cargarOrdenes() {
        console.log("Botón presionado");/* 
        const texto = document.getElementById("texto").value.trim();
        const semihemisferio = document.getElementById("semihemisferio").value;
        const params = new URLSearchParams(); */
/* 
        if (texto !== "") {
            params.append("texto", texto);
        }
        if (semihemisferio !== "Seleccionar") {
            params.append("semihemisferio", semihemisferio);
        }
         */
        const response = await fetch(`${host}/api/ordenes?${params.toString()}`);
        console.log(response);
        if (!response.ok) throw new Error("No encontró API");
        const ordenes = await response.json();
        console.log(ordenes);
        creacionLocales(ordenes);
}