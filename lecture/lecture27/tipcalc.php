<?php
    // get the data from the form
    $cost = $_POST['mcost'];
    $tiprate = $_POST['ptip'];
   

    // calculate tip
    $tip = $cost * ($tiprate * 0.01);
    

    // apply currency and percent formatting
    $cost_f = '$'.number_format($cost, 2);
    $tiprate_f = number_format($tiprate, 1);
    $tip_f = '$'.number_format($tip, 2);

?>
<!DOCTYPE html>
<head>
    <title>Tip Calculator</title>
    <link rel="stylesheet" type="text/css" href="main.css"/>
</head>
<body>
    <div id="content">
        <h1>Tip Calculator</h1>

        <label>Meal Cost:</label>
        <span><?php echo $cost_f; ?></span><br />

        <label>Percent Tip:</label>
        <span><?php echo $tiprate_f; ?></span><br />

        <label>Tip for Service:</label>
        <span><?php echo $tip_f; ?></span><br />

    </div>
</body>
</html>
