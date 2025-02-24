const API_URL = "http://127.0.0.1:5000/students"

function getStudents(){
    fetch(API_URL)
        .then(response => response.json())
        .then(data =>{
            console.log("Fetched students:", data);
            let table = document.getElementById("student-table");
            table.innerHTML = "";
            data.forEach(student => {
                table.innerHTML += `
                    <tr>
                        <td>${student.NAME}</td>
                        <td>${student.BRANCH}</td>
                        <td>${student.ROLL}</td>
                        <td>${student.SECTION}</td>
                        <td>${student.AGE}</td>
                        <td>
                            <button onclick="updateStudent(${student.ROLL})">Update</button>
                            <button onclick="deleteStudent(${student.ROLL})">Delete</button>
                        </td>
                    </tr>
                    `;
                
            });
        })
        .catch(error => console.error("Error fetching students: ", error))
}