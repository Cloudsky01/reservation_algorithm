

/*
*    DEFINITIONS
* RES_GOLFOCLOCK = reservation golfoclock (plusieurs rooms etc)
* res_opti = reservation pour l'optimisateur avec seulement 1 room
*/


reservations.forEach((RES_GOLFOCLOCK) => {

    RES_GOLFOCLOCK.solutions.forEach((sol, j) => {

        /* ajouter une variable bool   "sol_i_j"   au model ici */

        const sumDesVariablesAssignement = []
        for (let i = 0; i < sol.length; i++) { // ici on va loop sol.length fois ( == au nombre de rooms qu'il y a dans la RES_GOLFOCLOCK donc == au nombre de res_opti qui sont associée à cette RES_GOLFOCLOCK )
            const room_r = sol[i]
            const res_opti_i = RES_GOLFOCLOCK.getRes_opti_correspondant_au_bon_id_selon_i(i) //ici tu te debrouilles selon pour retrouver le bon id de la bonne res_opti qui est la sous res de RES_GOLFOCLOCK
            sumDesVariablesAssignement.push(variableAssignement_de_la_res_opti_i_assignée_à_la_room_r)
        }

        /**ajouter cette contrainte au model ici:   sumDesVariablesAssignement >= "sol_i_j"          (variable bool déclaré plus haut dans la meme iteration de cette boucle) */
    });
});




