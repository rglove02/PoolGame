#include "phylib.h"

#include <stdio.h>
#include <math.h>

void phylib_print_object( phylib_object *object )
{
  if (object==NULL)
  {
    printf( "NULL;\n" );
    return;
  }

  switch (object->type)
  {
    case PHYLIB_STILL_BALL:
      printf( "STILL_BALL (%d,%6.1lf,%6.1lf)\n",
	      object->obj.still_ball.number,
	      object->obj.still_ball.pos.x,
	      object->obj.still_ball.pos.y );
      break;

    case PHYLIB_ROLLING_BALL:
      printf( "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)\n",
              object->obj.rolling_ball.number,
              object->obj.rolling_ball.pos.x,
              object->obj.rolling_ball.pos.y,
              object->obj.rolling_ball.vel.x,
              object->obj.rolling_ball.vel.y,
              object->obj.rolling_ball.acc.x,
              object->obj.rolling_ball.acc.y );
      break;

    case PHYLIB_HOLE:
      printf( "HOLE (%6.1lf,%6.1lf)\n",
	      object->obj.hole.pos.x,
	      object->obj.hole.pos.y );
      break;

    case PHYLIB_HCUSHION:
      printf( "HCUSHION (%6.1lf)\n",
	      object->obj.hcushion.y );
      break;

    case PHYLIB_VCUSHION:
      printf( "VCUSHION (%6.1lf)\n",
	      object->obj.vcushion.x );
      break;
  }
}

void phylib_print_table( phylib_table *table )
{
  if (!table)
  {
    printf( "NULL\n" );
    return ;
  }

  printf( "time = %6.1lf;\n", table->time );
  for ( int i=0; i<PHYLIB_MAX_OBJECTS; i++ )
  {
    printf( "  [%02d] = ", i );
    phylib_print_object( table->object[i] );
  }

}

//given --------------------------------------------------------------------------------------------------------------------------------------------------------------------
int main( int argc, char **argv )
{
  phylib_coord pos, vel, acc;
  phylib_table *table;
  phylib_object *sb;
  phylib_object *rb;

  table = phylib_new_table();

  // create a still ball 1/4 of the way "down" the middle of the table,
  // shift it up, and to the left just a little bit
  pos.x = PHYLIB_TABLE_WIDTH / 2.0 
          - sqrt( PHYLIB_BALL_DIAMETER*PHYLIB_BALL_DIAMETER / 2.0 );
  pos.y = PHYLIB_TABLE_WIDTH / 2.0
          - sqrt( PHYLIB_BALL_DIAMETER*PHYLIB_BALL_DIAMETER / 2.0 );
  sb = phylib_new_still_ball( 1, &pos );

  // create a rolling ball 3/4 of the way "down the table,
  // rolling up along the centre
  pos.x = PHYLIB_TABLE_WIDTH / 2.0;
  pos.y = PHYLIB_TABLE_LENGTH - PHYLIB_TABLE_WIDTH / 2.0;
  vel.x = 0.0;
  vel.y = -1000.0; // 1m/s (medium speed)
  acc.x = 0.0;
  acc.y = 180.0;
  rb = phylib_new_rolling_ball( 0, &pos, &vel, &acc );

  phylib_add_object( table, sb );
  phylib_add_object( table, rb );

  phylib_print_table( table );

  // phylib_table *new = phylib_copy_table(table );
  // printf("AFTER copy");
  // phylib_print_table( new );

   do{
     phylib_table *new = phylib_segment( table );
     phylib_free_table( table );
     table = new;

     phylib_print_table( table );
   } while( table );
}


//Emily's ----------------------------------------------------------------------------------------------------------------------------------------------------------------
// int main( int argc, char **argv )
// {
//   phylib_table *table;
//   phylib_object *rb1 = phylib_new_rolling_ball(0, &(phylib_coord){PHYLIB_TABLE_WIDTH/2.0, PHYLIB_TABLE_WIDTH},
//                                                &(phylib_coord){1000.0, 0.0},
//                                                &(phylib_coord){-5.0, 0.0});
//   phylib_object *sb1 = phylib_new_still_ball(0, &(phylib_coord){PHYLIB_TABLE_WIDTH+200, PHYLIB_TABLE_WIDTH});      

//   table = phylib_new_table();
//   phylib_add_object( table, rb1 );
//   phylib_add_object( table, sb1 );
  

//   phylib_print_table( table );

//   do
//   {
//     phylib_table *new = phylib_segment( table );
//     phylib_free_table( table );
//     table = new;

//     phylib_print_table( table );
//   } while( table );

// }

//Emily Pt2 -------------------------------------------------------------------------------------------------------------------------------------------
// void test_phylib_sub() {
//     phylib_coord c1 = {10.0, 20.0};
//     phylib_coord c2 = {5.0, 10.0};
//     phylib_coord result = phylib_sub(c1, c2);

//     printf("Test phylib_sub:\n");
//     printf("Test Case 1:\n");
//     printf("c1 = (%.1lf, %.1lf)\n", c1.x, c1.y);
//     printf("c2 = (%.1lf, %.1lf)\n", c2.x, c2.y);
//     printf("Result = (%.1lf, %.1lf)\n", result.x, result.y);
//     printf("\n");
// }

// void test_phylib_length() {
//     phylib_coord c = {3.0, 4.0};
//     double length = phylib_length(c);

//     printf("Test phylib_length:\n");
//     printf("Test Case 1:\n");
//     printf("c = (%.1lf, %.1lf)\n", c.x, c.y);
//     printf("Length = %.1lf\n", length);
//     printf("\n");
// }

// void test_phylib_dot_product() {
//     phylib_coord a = {2.0, 3.0};
//     phylib_coord b = {4.0, 5.0};
//     double dotProduct = phylib_dot_product(a, b);

//     printf("Test phylib_dot_product:\n");
//     printf("Test Case 1:\n");
//     printf("a = (%.1lf, %.1lf)\n", a.x, a.y);
//     printf("b = (%.1lf, %.1lf)\n", b.x, b.y);
//     printf("Dot Product = %.1lf\n", dotProduct);
//     printf("\n");
// }

// int main() {
//     test_phylib_sub();
//     test_phylib_length();
//     test_phylib_dot_product();

//     return 0;
// }

//Emily Pt3 ---------------------------------------------------------------------------------------------------------------------------------------------------------------
// int main( int argc, char **argv )
// {
//   phylib_table *table;
//   phylib_object *rb1 = phylib_new_rolling_ball(0, &(phylib_coord){PHYLIB_TABLE_WIDTH/2.0, PHYLIB_TABLE_WIDTH},
//                                                &(phylib_coord){500.0, 0.0},
//                                                &(phylib_coord){-180.0, 0.0});
//   phylib_object *sb1 = phylib_new_still_ball(1, &(phylib_coord){PHYLIB_TABLE_WIDTH-200, PHYLIB_TABLE_WIDTH});    

//   table = phylib_new_table();

//   phylib_add_object( table, sb1 );
//   phylib_add_object( table, rb1 );
  

//   phylib_print_table( table );
//   printf("==============================\n");
//   printf("TEST 1\n");
//   printf("==============================\n");
//   do
//   {
//     phylib_table *new = phylib_segment( table );
//     phylib_free_table( table );
//     table = new;

//     phylib_print_table( table );
//   } while( table );

//   printf("==============================\n");
//   printf("TEST 2\n");
//   printf("==============================\n");
//   phylib_object *rb2 = phylib_new_rolling_ball(2, &(phylib_coord){PHYLIB_TABLE_WIDTH/2.0, PHYLIB_TABLE_WIDTH},
//                                                &(phylib_coord){830.0, 450.0},
//                                                &(phylib_coord){-100.0, -100.0});
//   table = phylib_new_table();
//   phylib_add_object(table,rb2);                
//   phylib_print_table(table);                             
//   do
//   {
//     phylib_table *new = phylib_segment( table );
//     phylib_free_table( table );
//     table = new;

//     phylib_print_table( table );
//   } while( table );
//   printf("==============================\n");
//   printf("TEST 3\n");
//   printf("==============================\n");

//   phylib_object *rb3 = phylib_new_rolling_ball(3, &(phylib_coord){800, 1625},
//                                                &(phylib_coord){830.0, 450.0},
//                                                &(phylib_coord){-100.0, -100.0});

//   table = phylib_new_table();
//   phylib_add_object(table,rb3);                
//   phylib_print_table(table);                             
//   do
//   {
//     phylib_table *new = phylib_segment( table );
//     phylib_free_table( table );
//     table = new;

//     phylib_print_table( table );
//   } while( table );                                          
// }

// CIS 2750 Assignment 1 ------------------------------------------------------------------------------------------------------------------------------------------------------
// Test Cases By: Pog

// void test_assert(char *str, double expected, double actual)
// {
//   double rexp = (round(expected * 1000) / 1000);
//   double ract = (round(actual * 1000) / 1000);
//   char *pass = (rexp == ract) ? "PASSED" : "FAILED";
//   fprintf(stdout, "\nTEST: %s - [%s]\n", str, pass);
//   fprintf(stdout, "==============================\n");
//   fprintf(stdout, "Expected Result: %f Actual Result: %f \n", rexp, ract);
//   fprintf(stdout, "==============================\n");
// }

// void test_print(char *str)
// {
//   fprintf(stdout, "\nTEST: %s\n", str);
//   fprintf(stdout, "==============================\n");
// }

// int main(int argc, char **argv)
// {
//   phylib_object *rb1 = phylib_new_rolling_ball(0, &(phylib_coord){100.0, 100.0},
//                                                &(phylib_coord){775.0, 775.0},
//                                                &(phylib_coord){125.0, 125.0});
//   phylib_object *rb1c = phylib_new_rolling_ball(0, &(phylib_coord){100.0, 100.0},
//                                                 &(phylib_coord){775.0, 775.0},
//                                                 &(phylib_coord){125.0, 125.0});
//   phylib_object *rb2 = phylib_new_rolling_ball(1, &(phylib_coord){250.0, 250.0},
//                                                &(phylib_coord){5.0, 5.0},
//                                                &(phylib_coord){-100.0, -100.0});
//   phylib_object *rb2c = phylib_new_rolling_ball(1, &(phylib_coord){250.0, 250.0},
//                                                 &(phylib_coord){5.0, 5.0},
//                                                 &(phylib_coord){-100.0, -100.0});
//   phylib_object *rb3 = phylib_new_rolling_ball(2, &(phylib_coord){500.0, 1000.0},
//                                                &(phylib_coord){-100.0, 0.0},
//                                                &(phylib_coord){5.0, 0.0});
//   phylib_object *rb4 = phylib_new_rolling_ball(3, &(phylib_coord){400.0, 500.0},
//                                                &(phylib_coord){100.0, 250.0},
//                                                &(phylib_coord){50.0, 50.0});
//   phylib_object *rb5 = phylib_new_rolling_ball(3, &(phylib_coord){425.0, 500.0},
//                                                &(phylib_coord){10.0, 250.0},
//                                                &(phylib_coord){50.0, 50.0});
//   phylib_object *sb1 = phylib_new_still_ball(0, &(phylib_coord){100.0, 100.0});
//   phylib_table *table = phylib_new_table();

//   // phylib_roll test 1
//   phylib_roll(rb1c, rb1, 10.0 * PHYLIB_SIM_RATE);
//   test_assert("Rolling Ball - pos.x", 100.775, rb1c->obj.rolling_ball.pos.x);
//   test_assert("Rolling Ball - vel.y", 775.125, rb1c->obj.rolling_ball.vel.y);

//   // phylib_roll test 2 - velocity switch
//   phylib_roll(rb2c, rb2, 1.0);
//   test_assert("Rolling Ball - vel.x", 0.000, rb2c->obj.rolling_ball.vel.x);
//   test_assert("Rolling Ball - acc.y", 0.000, rb2c->obj.rolling_ball.acc.y);
//   test_assert("Rolling Ball - stopped", 1, phylib_stopped(rb2c));

//   // phylib_bounce test 1 - cushion
//   phylib_add_object(table, rb3);
//   phylib_table *ret_table = phylib_segment(table);
//   phylib_free_table(table);
//   table = ret_table;
//   test_assert("Bounce - pos.x", 28.500, table->object[10]->obj.rolling_ball.pos.x);
//   test_assert("Bounce - vel.x", 72.698, table->object[10]->obj.rolling_ball.vel.x);
//   test_assert("Bounce - time", 5.460, table->time);

//   // phylib_bounce test 2 - still_ball
//   ret_table = phylib_segment(table);
//   phylib_free_table(table);
//   table = ret_table;
//   test_assert("Segment - stop time", 19.998, table->time);
//   test_assert("Segment - stop pos.x", 557.0, table->object[10]->obj.rolling_ball.pos.x);
//   test_assert("Segment - rolling", 0, phylib_rolling(table));
//   // phylib_bounce test 3 - hole
//   phylib_add_object(table, rb4);
//   for (int i = 0; i < 4; i++)
//   {
//     ret_table = phylib_segment(table);
//     phylib_free_table(table);
//     table = ret_table;
//   }
//   test_assert("Segment - hole ball pos.x", 557.0, table->object[10]->obj.rolling_ball.pos.x);
//   test_assert("Segment - time", 27.676, table->time);
//   test_assert("Segment - rolling", 0, phylib_rolling(table));
//   // phylib_bounce test 4 - rolling
//   phylib_add_object(table, rb5);
//   ret_table = phylib_segment(table);
//   phylib_free_table(table);
//   table = ret_table;
//   phylib_rolling_ball ball2 = table->object[10]->obj.rolling_ball;
//   phylib_rolling_ball ball3 = table->object[11]->obj.rolling_ball;
//   test_assert("Segment Bounce - Ball 2 vel.x", 210.580, ball2.vel.x);
//   test_assert("Segment Bounce - Ball 2 vel.y", 117.668, ball2.vel.y);
//   test_assert("Segment Bounce - Ball 2 acc.x", -130.944, ball2.acc.x);
//   test_assert("Segment Bounce - Ball 2 acc.y", -73.169, ball2.acc.y);
//   test_assert("Segment Bounce - Ball 3 pos.x", 507.247, ball3.pos.x);
//   test_assert("Segment Bounce - Ball 3 pos.y", 972.199, ball3.pos.y);
//   test_assert("Segment Bounce - Ball 3 vel.x", -119.340, ball3.vel.x);
//   test_assert("Segment Bounce - Ball 3 vel.y", 213.572, ball3.vel.y);
//   test_assert("Segment Bounce - Ball 3 acc.x", 73.169, ball3.acc.x);
//   test_assert("Segment Bounce - Ball 3 acc.y", -130.944, ball3.acc.y);
//   test_assert("Segment Bounce - Time", 29.301, table->time);

//   // Check for Memory Leaks if segment returns null (no balls rolling)
//   test_print("phylib_segment no balls rolling memory test");
//   phylib_add_object(table, sb1);
//   for (int i = 0; i < 3; i++)
//   {
//     ret_table = phylib_segment(table);
//     phylib_free_table(table);
//     table = ret_table;
//   }
//   phylib_print_table(table);
//   free(rb1);
//   free(rb2);
//   free(rb1c);
//   free(rb2c);
// }


//Colins ------------------------------------------------------------------------------------------------------------------------------------------------------
//keep for all below
// int main( int argc, char **argv )
// {
//   phylib_coord pos, vel, acc;
//   phylib_table *table;
//   phylib_object *sb = NULL;
//   phylib_object *rb = NULL;

//   table = phylib_new_table();

// ALL of the test are documented in the graphs below and will show what the test is
// https://www.desmos.com/calculator/hmnvf2ocyd


//TEST #1 (GIVEN) --------------------------------------------------------------------------------------------------------------
	
  // // create a still ball 1/4 of the way "down" the middle of the table,
  // // shift it up, and to the left just a little bit
  // pos.x = PHYLIB_TABLE_WIDTH / 2.0 - sqrt( PHYLIB_BALL_DIAMETER*PHYLIB_BALL_DIAMETER / 2.0 );
  // pos.y = PHYLIB_TABLE_WIDTH / 2.0- sqrt( PHYLIB_BALL_DIAMETER*PHYLIB_BALL_DIAMETER / 2.0 );
  // sb = phylib_new_still_ball( 1, &pos );

  // // create a rolling ball 3/4 of the way "down the table,
  // // rolling up along the centre
  // pos.x = PHYLIB_TABLE_WIDTH / 2.0;
  // pos.y = PHYLIB_TABLE_LENGTH - PHYLIB_TABLE_WIDTH / 2.0;
  // vel.x = 0.0;
  // vel.y = -1000.0; // 1m/s (medium speed)
  // acc.x = 0.0;
  // acc.y = 180.0;
  // rb = phylib_new_rolling_ball( 0, &pos, &vel, &acc );

  // phylib_add_object( table, sb );
  // phylib_add_object( table, rb );


//2 (WRONG?)-----------------------------------------------------------------------------------------------------------------------------
  // pos.x = PHYLIB_TABLE_WIDTH/2;
  // vel.x = 1000.0; // 1m/s (medium speed)
  // vel.y = 0.0; 
  // acc.x = -180.0;
  // acc.y = 0.0;
  // rb = phylib_new_rolling_ball( 0, &pos, &vel, &acc );
  
  // phylib_add_object( table, rb );
  
//3 -----------------------------------------------------------------------------------------------------------------------
//see desmos for layout
  // pos.x = PHYLIB_TABLE_WIDTH - 200;
  // pos.y =  PHYLIB_TABLE_WIDTH;
  // sb = phylib_new_still_ball( 69, &pos );
  
  // pos.x = PHYLIB_TABLE_WIDTH/2;
  // vel.x = 1000.0; // 1m/s (medium speed)
  // vel.y = 0.0; 
  // acc.x = -180.0;
  // acc.y = 0.0;
  // rb = phylib_new_rolling_ball( 0, &pos, &vel, &acc );

  // phylib_add_object( table, sb );
  // phylib_add_object( table, rb );

//4 -------------------------------------------------------------------------------------------------------------------------------
// We will attempt to do a tripple bounce where the ball will hit three walls and then come to a stop without going into a hole
  // pos.y =  PHYLIB_TABLE_WIDTH;
  
  // pos.x = PHYLIB_TABLE_WIDTH/2;
  // vel.x = 1000.0; // 1m/s (medium speed)
  // vel.y = 500.0; 
  // acc.x = -180.0;
  // acc.y = -90.0;
  // rb = phylib_new_rolling_ball( 0, &pos, &vel, &acc );

  // phylib_add_object( table, rb );

//5 ------------------------------------------------------------------------------------------------------------------------------------
  // pos.y =  1625;
  
  // pos.x = 800;
  // vel.x = -1000.0; // 1m/s (medium speed)
  // vel.y = 500.0; 
  // acc.x = 180.0;
  // acc.y = -90.0;
  // rb = phylib_new_rolling_ball( 0, &pos, &vel, &acc );

  
  // phylib_add_object( table, rb );

//6 -----------------------------------------------------------------------------------------------------------------------------------------------
  // pos.y =  1625;
  
  // pos.x = 800;
  // vel.x = -1000.0; // 1m/s (medium speed)
  // vel.y = 500.0; 
  // acc.x = 180.0;
  // acc.y = -90.0;
  // rb = phylib_new_rolling_ball( 69, &pos, &vel, &acc );
  
  // pos.y =  2346.5; 
  // pos.x = 700;
  // sb = phylib_new_still_ball( 42, &pos );
  
  // phylib_add_object( table, rb );
  // phylib_add_object( table, sb );

	// phylib_print_table( table );

  //keep for all below
  // do
  // {
  //   phylib_table *new = phylib_segment( table );
  //   phylib_free_table( table );
  //   table = new;

  //   phylib_print_table( table );
  // } while( table ); 

// }
