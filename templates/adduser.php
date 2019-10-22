<?php

//Block 1
$user = "tiffany"; //Enter the user name
$password = "fannytea"; //Enter the password
$host = "127.0.0.1"; //Enter the host
$dbase = "foldoverdata.db"; //Enter the database
$table = "users"; //Enter the table name

//Block 2
$firstname= $_POST['firstname_entered'];
$lastname= $_POST['lastname_entered'];
$email= $_POST['email_entered'];

//Block 3
$connection= mysql_connect ($host, $user, $password);
if (!$connection)
{
die ('Could not connect:' . mysql_error());
}
mysql_select_db($database, $connection);


//Block 4
$username_table= mysql_query( "SELECT username FROM $table WHERE username= '$username'" )
or die("SELECT Error: ".mysql_error());


//Block 5
mysql_query("INSERT INTO $table (column1, column2, column3)
VALUES (value1, value2, value 3)");

//Block 6
echo 'You have been added.';

//Block 7
mysql_close($connection);

?>
