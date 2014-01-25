<?php

function sendSingleSMS($twilioPhoneNumber, $phoneNumberToSMS, $message) {

    //fixes phone numbers by appending a +1 the front if it does not have one
//    $twilioPhoneNumber = twilioifyPhoneNumber($twilioPhoneNumber);
//    $phoneNumberToSMS = twilioifyPhoneNumber($phoneNumberToSMS);
    //include_once $_SERVER['DOCUMENT_ROOT'] . '/EDI/twilio-php/Services/Twilio.php';
    $account_sid = "AC9538472cddf54050bb102f8a36da3189"; // Your Twilio account sid
    $auth_token = "5471b91d409e2d3484770165f439f75c"; // Your Twilio auth token
    //$callBackURL = 'http://egov.broomfield.org/EDI/reply/replySMS.php';
    // resource url & authentication
    $url = 'https://api.twilio.com/2010-04-01/Accounts/' . $account_sid . '/SMS/Messages.json';
    $auth = $account_sid . ':' . $auth_token;
    $type = 'sms';
    $curlError = '';
    $fullResults = '';

    //This code splits the SMS message into an array so that each message is under 160 characters 
    //so EDI can actually send it to Twilio.
    $chunks = explode("||||", wordwrap($message, 155, "||||", false));
    $total = count($chunks);
    $currentChunk = 0;
    //echo "total chunks are : $total";

    foreach ($chunks as $individualSMS) {

        try {
            // post string (phone number format= +15554443333 ), case matters
            $fields =
                    '&To=' . urlencode($phoneNumberToSMS) .
                    '&From=' . urlencode($twilioPhoneNumber) .
                    '&Body=' . urlencode($individualSMS) ;
                   // '&StatusCallback=' . urlencode($callbackURL);

            // start cURL
            $ch = curl_init();

            // set cURL options
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_POST, 3); // number of fields
            curl_setopt($ch, CURLOPT_POSTFIELDS, $fields);
            curl_setopt($ch, CURLOPT_USERPWD, $auth); // authenticate
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE); //don't comment this out :)
            //------------Optional paramaters ----------------------------------
            curl_setopt($ch, CURLOPT_FRESH_CONNECT, true); //added
            curl_setopt($ch, CURLOPT_NOSIGNAL, 1); //added
            //curl_setopt($ch, CURLOPT_TIMEOUT_MS, 40); //cuts send/response time so the process doesnt have to wait
            //curl_setopt( $res, CURLOPT_RETURNTRANSFER, true ); // don't echo
            //------------------------------------------------------------------
            // send cURL, capture results (if any)
            $results = curl_exec($ch);

            //example of json returned by Twilio results:
            //{"sid":"SM016927cc2a0e3820865695bcdc327e34","date_created":"Thu, 25 Oct 2012 16:04:56 +0000","date_updated":"Thu, 25 Oct 2012 16:04:56 +0000","date_sent":null,"account_sid":"AC9538472cddf54050bb102f8a36da3189","to":"+13038775964","from":"+17204142570","body":"some message that is way longer than 160 characters so that we can chunk the damn thing into oblivion.\n This still wasn't over 160 characters so now it","status":"queued","direction":"outbound-api","api_version":"2010-04-01","price":null,"uri":"\/2010-04-01\/Accounts\/AC9538472cddf54050bb102f8a36da3189\/SMS\/Messages\/SM016927cc2a0e3820865695bcdc327e34.json"}
            //Enable to see curl errors.
            if (curl_errno($ch)) {
                $curlError = 'error: ' . curl_error($ch);
            }

            //grabs returned info from Twilio and dumps into array
            $array = json_decode($results, true);

            $fullResults = $fullResults . " " . $results . $curlError;
            curl_close($ch);

            //set the SID for 
            if (!isset($array["sid"])) {
                $sid = '';
            } else {
                $sid = $array["sid"];
            }

            $currentChunk++;
        } catch (Exception $e) {
            $error = 'Oh my, this is embarrasing.  We just had an error in our pants when trying to send an SMS.' . $e->getMessage();
            echo $error;
            exit();
        }
    }


    return $fullResults;
}
?>
