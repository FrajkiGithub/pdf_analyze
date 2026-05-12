<?php
// Skript pro počítadlo návštěv
$soubor_pocitadla = 'pocitadlo.txt';
if (!file_exists($soubor_pocitadla)) {
    file_put_contents($soubor_pocitadla, '0');
}
$pocet_navstev = (int)file_get_contents($soubor_pocitadla);
$pocet_navstev++;
file_put_contents($soubor_pocitadla, $pocet_navstev);
?>
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Analyzátor PDF | Quatro</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="style.min.css">
    
    <link rel="shortcut icon" href="favicon.ico">
    
    <style>
        :root {
            --brand-blue: #264796;
            --bg-light: #f4f6f9;
            --bg-white: #ffffff;
        }

        html, body {
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            font-family: 'Manrope', sans-serif;
            background-color: var(--bg-light);
        }

        header {
            background-color: var(--brand-blue);
            padding: 15px 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        header img {
            max-height: 50px;
            width: auto;
        }

        .content-wrapper {
            flex: 1;
            display: flex;
            flex-direction: column;
            width: 80%;
            max-width: 1400px;
            margin: 40px auto;
            background-color: var(--bg-white);
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            overflow: hidden;
        }

        .app-header {
            padding: 25px 30px 15px 30px;
            border-bottom: 1px solid #eee;
        }

        .app-header h1 {
            margin: 0 0 10px 0;
            color: var(--brand-blue);
            font-size: 28px;
            font-weight: 800;
        }

        .app-header p {
            margin: 0;
            color: #555;
            font-size: 15px;
        }

        .iframe-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            width: 100%;
            min-height: 500px;
        }

        iframe {
            flex: 1;
            width: 100%;
            height: 100%;
            border: none;
            display: block;
        }

        footer {
            background-color: var(--brand-blue);
            color: #ffffff;
            padding: 15px 30px;
            font-size: 14px;
            margin-top: auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .footer-content {
            opacity: 0.9;
        }

        .footer-counter {
            opacity: 0.7;
            font-size: 13px;
        }
    </style>
</head>
<body>

    <header>
        <img src="header-logo.svg" alt="Logo Quatro">
    </header>

    <main class="content-wrapper">
        
        <div class="app-header">
            <h1>Souborový analyzátor</h1>
            <p>Nahrajte soubory pro okamžitý výpočet rozměrů a plochy.</p>
        </div>

        <div class="iframe-container">
            <iframe 
                src="https://pdfanalyze-buugmkahgdaljtn4gipkms.streamlit.app/?embed=true&embed_options=show_toolbar=false,show_padding=false"
                allow="downloads">
            </iframe>
        </div>

    </main>

    <footer>
        <div class="footer-content">
            © 2026 QUATRO
        </div>
        <div class="footer-counter">
            Zobrazeno: <?php echo $pocet_navstev; ?>x
        </div>
    </footer>

</body>
</html>