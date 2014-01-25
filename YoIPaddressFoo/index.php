<?php

//This code sends an SMS to the phone number listed below 
//when this page is hit with a 'get' and the token is set
//Roy Stillwell
//Oct 29 2013

if (isset($_POST['token']) && $_POST['token'] == 'supersecretsauce') {
    require_once $_SERVER['DOCUMENT_ROOT'] . '/YoIPaddressFoo/Includes/SMSlibrary.lib.php';
    
    $arrayOfNumbers = array("3038775964", "7203846332", "7202190299", "7202788668");
    //$arrayOfNumbers = array("3038775964");
    //Roy, Drew, Martin, Thomas - Parking dudes
    $twilioPhoneNumber = "+13038359480"; //A phone number for Twilio in Roy's account at CCOB
    $ipaddress = shell_exec ("/sbin/ifconfig wlan0 | grep 'inet addr:'|cut -d: -f2 | awk '{print $1}'");
    //$ipaddress = shell_exec ("/sbin/ifconfig wlan0");
    $message = "Yo Pi IP Address Foo! -> " . $ipaddress;
    echo $ipaddress; 
foreach ($arrayOfNumbers as $phoneNumberToSMS) {
        echo "Numbers sent are: $phoneNumberToSMS /n";
        sendSingleSMS($twilioPhoneNumber, $phoneNumberToSMS, $message);
    }
    echo "All messages sent!";
} else {
    echo "The proper key was not sent to send an SMS! Wah wah";
}
//curl post to send curl --data "token=supersecretsauce" http://localhost/YoIPaddressFoo/index.php
// sleep
?>
