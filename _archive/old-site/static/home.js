document.addEventListener("DOMContentLoaded", function() {
    const namesearch = document.getElementById('name-search')
    const tagsearch = document.querySelectorAll(".tag")
    const project = document.querySelectorAll(".project")

    function filterprojects() { 
        const namequery = namesearch.value.toLowerCase();
    
        project.forEach ((project) => {
            const name = project.getAttribute('data-name')
            const nameMatch = name.includes(namequery)

            if (nameMatch) {
                project.style.display = "";
            } else {
                project.style.display = "none";
            }


            })
        }     
        
        tagsearch.forEach((tag) => {
            tag.addEventListener("click", function() {
                const selectedTag = this.getattribute("data-tag");
                project.forEach((project) => {
                    const projectTags = project.getAttribute("data-tag")
                    if (projectTags.includes(selectedTag)) {
                        project.style.display = "";
                    } else {
                        project.style.display = "none";
                    }
                })

            })
        })

    nameSearch.addEventListener("keyup", filterprojects)
    })
