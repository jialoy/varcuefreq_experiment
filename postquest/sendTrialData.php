<?php
if(!empty($_POST['data'])){
    
    $data = $_POST['data'];
    
    list($fileID, $trialData) = explode('+', $data);
    
    $file = '/home/jloy/server_data/cuelearning_postquest_data/' . $fileID . '.csv';
    
    file_put_contents($file, $trialData, FILE_APPEND | LOCK_EX);
}
?>