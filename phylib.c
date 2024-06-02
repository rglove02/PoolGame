#include "phylib.h"

//PT1
//Function prototypes for constructor methods
phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ){
    
    //create new object
    phylib_object *newObject = malloc(sizeof(phylib_object));

    if(newObject == NULL){
        //return null if malloc did not work
        return NULL;
    } 

    //create pointer
    phylib_still_ball *pointerStillBall;

    //link it to newObject
    newObject->type = PHYLIB_STILL_BALL;
    pointerStillBall = &newObject->obj.still_ball;

    //set what it holds
    pointerStillBall->number = number;
    pointerStillBall->pos = *pos;

    //return address
    return newObject;  

}

phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ){
    
    //create new object
    phylib_object *newObject = malloc(sizeof(phylib_object));

    if(newObject == NULL){
        //return null if malloc does not work
        return NULL;
    }

    //create pointer
    phylib_rolling_ball *pointerRollBall;

    //link it to newObject
    newObject->type = PHYLIB_ROLLING_BALL;
    pointerRollBall = &newObject->obj.rolling_ball;

    //set what it holds
    pointerRollBall->number = number;
    pointerRollBall->pos = *pos;
    pointerRollBall->vel = *vel;
    pointerRollBall->acc = *acc;

    //return address
    return newObject;
      
}

phylib_object *phylib_new_hole( phylib_coord *pos ){
    
    //create new object
    phylib_object *newObject = malloc(sizeof(phylib_object));

    if(newObject == NULL){
        //return null if malloc does not work
        return NULL;
    } 

    //create pointer
    phylib_hole *pointerHole;

    //link it to newObject
    newObject->type = PHYLIB_HOLE;
    pointerHole = &newObject->obj.hole;

    //set what it holds
    pointerHole->pos = *pos;

    //return address
    return newObject;
}

phylib_object *phylib_new_hcushion( double y ){
    
    //create new object
    phylib_object *newObject = malloc(sizeof(phylib_object));

    if(newObject == NULL){
        //return null if malloc does not work
        return NULL;
    } 

    //create pointer
    phylib_hcushion *pointerHCushion;

    //link it to newObject
    newObject->type = PHYLIB_HCUSHION;
    pointerHCushion = &newObject->obj.hcushion;

    //set what it holds
    pointerHCushion->y = y;

    //return address
    return newObject;
}

phylib_object *phylib_new_vcushion( double x ){
    //create new object
    phylib_object *newObject = malloc(sizeof(phylib_object));

    if(newObject == NULL){
        //return null if malloc does not work
        return NULL;
    } 

    //create pointer
    phylib_vcushion *pointerVCushion;

    //link it to newObject
    newObject->type = PHYLIB_VCUSHION;
    pointerVCushion = &newObject->obj.vcushion;

    //set what it holds
    pointerVCushion->x = x;

    //return address
    return newObject;
}

phylib_table *phylib_new_table( void ){

    //create space for table struct
    phylib_table *table = malloc(sizeof(phylib_table));

    //check to make sure malloc worked
    if(table == NULL){
        return NULL;
    }

    //set values for the table
    table->time = 0.0;

    //add horizontal cushions
    table->object[0] = phylib_new_hcushion(0.0);
    table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);

    //add vertical cushions
    table->object[2] = phylib_new_vcushion(0.0);
    table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    //add holes
    phylib_coord pos;

    pos.x = 0.0;
    pos.y = 0.0;
    table->object[4] = phylib_new_hole(&pos);

    pos.x = 0.0;
    pos.y = PHYLIB_TABLE_WIDTH;
    table->object[5] = phylib_new_hole(&pos);

    pos.x = 0.0;
    pos.y = PHYLIB_TABLE_LENGTH;
    table->object[6] = phylib_new_hole(&pos);

    pos.x = PHYLIB_TABLE_WIDTH;
    pos.y = 0.0;
    table->object[7] = phylib_new_hole(&pos);

    pos.x = PHYLIB_TABLE_WIDTH;
    pos.y = PHYLIB_TABLE_WIDTH;
    table->object[8] = phylib_new_hole(&pos);

    pos.x = PHYLIB_TABLE_WIDTH;
    pos.y = PHYLIB_TABLE_LENGTH;
    table->object[9] = phylib_new_hole(&pos);

    // Set all the ball pointers to null
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++) {
        table->object[i] = NULL;
    }

    //return address
    return table;
}

//PT2
//Utility Functions
void phylib_copy_object( phylib_object **dest, phylib_object **src ){

    //allocate memory for the object
    *dest = malloc(sizeof(phylib_object));

    //check to make sure malloc worked
    if(*src == NULL || *dest == NULL){
        *dest = NULL;

    }else{

        //copy the object
        memcpy(*dest, *src, sizeof(phylib_object));
    }
}

phylib_table *phylib_copy_table( phylib_table *table ){

    //make space for the new table
    phylib_table *newTable = malloc(sizeof(phylib_table));

    //check to make sure that the table isn't null and malloc worked
    if(table == NULL || newTable == NULL){
        return NULL;
    }
    
    //copy the table
    memcpy(newTable, table, sizeof(phylib_table));

    //copies objects
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if (table->object[i] != NULL) {
            phylib_copy_object(&newTable->object[i], &table->object[i]);
        } else {
            newTable->object[i] = NULL;
        }
    }

    return newTable;
}

void phylib_add_object( phylib_table *table, phylib_object *object ){

    //goes through object and finds a null pointer
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i] == NULL){
            table->object[i] = object;
            break;
        }
    }
}

void phylib_free_table( phylib_table *table ){

    //goes through table and frees objects
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        free(table->object[i]);
        table->object[i] = NULL;
    }

    //frees the table
    free(table);
}

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){
    phylib_coord difference;

    //finding the difference
    difference.x = c1.x - c2.x;
    difference.y = c1.y - c2.y;

    return difference;
}

double phylib_length( phylib_coord c ){
    //Pythagorean Theorm: a^2 + b^2 = c^2
    return sqrt((c.x*c.x) + (c.y*c.y));
}

double phylib_dot_product( phylib_coord a, phylib_coord b ){
    //Dot Product: (x*x) + (y*y)
    return (a.x*b.x) + (a.y*b.y);
}

double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){

    //if the first object is not a rolling ball
    if(obj1->type != PHYLIB_ROLLING_BALL){
        return -1.0;
    }

    double distance = 0.0;
    phylib_coord c;

    //check if it is a ball, hole or cushion
    if(obj2->type == PHYLIB_ROLLING_BALL){
        c = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos);
        distance = phylib_length(c);

        distance -= PHYLIB_BALL_DIAMETER;

    } else if(obj2->type == PHYLIB_STILL_BALL){
        c = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos);
        distance = phylib_length(c);
        
        distance -= PHYLIB_BALL_DIAMETER;

    }else if(obj2->type == PHYLIB_HOLE){
        c = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos);
        distance = phylib_length(c);

        distance -= PHYLIB_HOLE_RADIUS;   

    } else if(obj2->type == PHYLIB_VCUSHION){
        distance = obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x;

        distance = fabs(distance);
        distance -= PHYLIB_BALL_RADIUS;

    }else if(obj2->type == PHYLIB_HCUSHION){
        distance = obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y;

        distance = fabs(distance);
        distance -= PHYLIB_BALL_RADIUS;
    }

    //return the distance between the objects
    return distance;
}

//PT3
//Functions to simulate the balls moving on the table
void phylib_roll( phylib_object *new, phylib_object *old, double time ){

    //makes sure both objects are rolling balls
    if ((old->type == PHYLIB_ROLLING_BALL) && (new->type == PHYLIB_ROLLING_BALL)){

        double newVelX = new->obj.rolling_ball.vel.x;
        double newVelY = new->obj.rolling_ball.vel.y;

        //calculate position
        //p = p1 + v1t +1/2 a1 t^2
        new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + (old->obj.rolling_ball.vel.x * time) + ((old->obj.rolling_ball.acc.x * time * time)/2.0); 
        new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + (old->obj.rolling_ball.vel.y * time) + ((old->obj.rolling_ball.acc.y * time * time)/2.0); 

        //calculate velocity
        //v = v1 + a1 t
        new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + (old->obj.rolling_ball.acc.x * time);
        new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y * time);
        
        //check to see if the velocity's sign changed
        //check x vel
        if((old->obj.rolling_ball.vel.x  * newVelX) < 0.0){
            new->obj.rolling_ball.vel.x = 0.0;
            new->obj.rolling_ball.acc.x = 0.0;
        } 

        //check y vel
        if((old->obj.rolling_ball.vel.y * newVelY) < 0.0){
            new->obj.rolling_ball.vel.y = 0.0;
            new->obj.rolling_ball.acc.y = 0.0; 
        } 
    }
}

unsigned char phylib_stopped( phylib_object *object ){

    double distance = phylib_length(object->obj.rolling_ball.vel);

    //check the velocity
    if(distance < PHYLIB_VEL_EPSILON){

        //set up temp variables
        phylib_coord pos = object->obj.rolling_ball.pos;

        unsigned char number;
        number = object->obj.rolling_ball.number;
        
        //change object type to a still ball
        object->type = PHYLIB_STILL_BALL;

        //change members
        object->obj.still_ball.number = number;
        object->obj.still_ball.pos = pos;

        return 1;
    }
    return 0;
}

void phylib_bounce( phylib_object **a, phylib_object **b ){

    //check to see what object b is
    if((*b)->type == PHYLIB_HCUSHION){
        //negate the y velocities and acceleration
        (*a)->obj.rolling_ball.vel.y = (-1.0) * (*a)->obj.rolling_ball.vel.y;
        (*a)->obj.rolling_ball.acc.y = (-1.0) * (*a)->obj.rolling_ball.acc.y;

    }else if((*b)->type == PHYLIB_VCUSHION){
        //negate the x velocities and acceleration
        (*a)->obj.rolling_ball.vel.x = (-1.0) * (*a)->obj.rolling_ball.vel.x;
        (*a)->obj.rolling_ball.acc.x = (-1.0) * (*a)->obj.rolling_ball.acc.x;

    }else if((*b)->type == PHYLIB_HOLE){
        //free object a and set to NULL (off the table)
        free(*a);
        (*a) = NULL;

    }else if((*b)->type == PHYLIB_STILL_BALL){

        //change to rolling ball function
        stillBallUpgrade(a,b);

        //goes to case 5 --> type = rolling ball (below)
    }

    //check to see if object b is a rolling ball
    if((*b)->type == PHYLIB_ROLLING_BALL){

        //do calculations to updave members function
        rollingBallCalc(a, b);
    } 
}

void rollingBallCalc(phylib_object **a, phylib_object **b){
    //calculate position of a
    //position a-b
    phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

    //calculate velocity of a
    //velocity b - a
    phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

    //calculate the normal
    //r_ab / r_ab length
    phylib_coord n;
    n.x = r_ab.x / phylib_length(r_ab);
    n.y = r_ab.y / phylib_length(r_ab);

    //ratio of velocity -> use dot product
    double v_rel_n = phylib_dot_product(v_rel, n);

    //update the x velocity of ball a
    //velocity - v_rel_n x normal
    (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x - v_rel_n * n.x;
    (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y - v_rel_n * n.y;

    //update the x velocity of ball b
    (*b)->obj.rolling_ball.vel.x = (*b)->obj.rolling_ball.vel.x + v_rel_n * n.x;
    (*b)->obj.rolling_ball.vel.y = (*b)->obj.rolling_ball.vel.y + v_rel_n * n.y;

    //calculate speed of a and b
    double speeda = phylib_length((*a)->obj.rolling_ball.vel);
    double speedb = phylib_length((*b)->obj.rolling_ball.vel);

    //set acceleration -> - velocity / speed * drag
    if(speeda > PHYLIB_VEL_EPSILON){
        (*a)->obj.rolling_ball.acc.x = (-1.0) * (*a)->obj.rolling_ball.vel.x / speeda * PHYLIB_DRAG;
        (*a)->obj.rolling_ball.acc.y = (-1.0) * (*a)->obj.rolling_ball.vel.y / speeda * PHYLIB_DRAG;

    }
    if(speedb > PHYLIB_VEL_EPSILON){
        (*b)->obj.rolling_ball.acc.x = (-1.0) * (*b)->obj.rolling_ball.vel.x / speedb * PHYLIB_DRAG;
        (*b)->obj.rolling_ball.acc.y = (-1.0) * (*b)->obj.rolling_ball.vel.y / speedb * PHYLIB_DRAG;
    }
}

void stillBallUpgrade(phylib_object **a, phylib_object **b){

    //set up temp variables
    phylib_coord pos = (*b)->obj.still_ball.pos;

    unsigned char number = 0;
    number = (*b)->obj.still_ball.number;

    //change type to a rolling ball
    (*b)->type = PHYLIB_ROLLING_BALL;

    //change members
    (*b)->obj.rolling_ball.number = number;
    (*b)->obj.rolling_ball.pos= pos;

    //add vel and acc members + set them to 0
    (*b)->obj.rolling_ball.vel.x = 0;
    (*b)->obj.rolling_ball.vel.y = 0;

    (*b)->obj.rolling_ball.acc.x = 0;
    (*b)->obj.rolling_ball.acc.y = 0; 
}

unsigned char phylib_rolling( phylib_table *t ){
   
    unsigned char number = 0;

    //goes through the table
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){

        //checks to see if it is a rolling ball
        if(t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL){
            number++;
        }
    }
    
    return number;
}

phylib_table *phylib_segment( phylib_table *table ){

    //checks to make sure that there are rolling balls
    if(phylib_rolling(table) <= 0){
        return NULL;
    }

    //make a copy of the table
    phylib_table *newTable = phylib_copy_table(table);

    //check to make sure malloc
    if(newTable == NULL){
        return NULL;
    }

    // set time variable
    double time = 0.0;

    //checks to see if hits max time
    while(time <= PHYLIB_MAX_TIME){

         //increase the time
        time += PHYLIB_SIM_RATE;

        //goes through the balls and rolls if applies
        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){

            //checks to see if it is a rolling ball
            if(newTable->object[i] != NULL && newTable->object[i]->type == PHYLIB_ROLLING_BALL){
                
                //applies rolling function
                phylib_roll(newTable->object[i],table->object[i],time);
            }
        }
        
        //check to see if a ball has stopped or hit something after all ablls have rolled
        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){

            //makes sure it is a rolling ball
            if(newTable->object[i] != NULL && newTable->object[i]->type == PHYLIB_ROLLING_BALL){

                //check if it hit another obj and
                //check if rolling ball stopped
                if(phylib_stopped(newTable->object[i]) || hitObj( newTable, i ) == true){

                    //adds time to table time
                    newTable->time += time;

                    //return the updated new table
                    return newTable;
                }
            }
        }
    }
    return newTable;
}

//checks to see if hit something
bool hitObj( phylib_table *newTable, int i ){

    //goes through the objects in table
    for(int j = 0; j < PHYLIB_MAX_OBJECTS; j++){

        //checks to see if it is the same object
        if(i != j && newTable->object[j] != NULL){

            //checks to see if they hit ->distnace between objects
            if(phylib_distance(newTable->object[i],newTable->object[j]) < 0.0){

                //handles the hit
                phylib_bounce(&newTable->object[i],&newTable->object[j]);
                
                return true;
            }
        }
    }
    return false;
}

//A2 new Func
char *phylib_object_string( phylib_object *object ){
    static char string[80];

    if (object==NULL){
        snprintf( string, 80, "NULL;" );
        return string;
    }

    switch (object->type){
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,
            object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            snprintf( string, 80,
            "HOLE (%6.1lf,%6.1lf)",
            object->obj.hole.pos.x,
            object->obj.hole.pos.y );
            break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80,
            "HCUSHION (%6.1lf)",
            object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80,
            "VCUSHION (%6.1lf)",
            object->obj.vcushion.x );
            break;
        }
    return string;
}
