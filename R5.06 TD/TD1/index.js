const express = require('express');
const app = express();
const PORT = 3000;
const fs = require('fs');
const path = require('path');



app.get('/', (req, res) => {
  res.send('Hello World');
});

app.listen(PORT, () => {
  console.log('Server is running on http://localhost:3000');
});

app.post('/upload', (req, res) => {
  // Code pour déposer un fichier
  // Ouverture d'un flux d'écriture vers un fichier file.txt dans le répertoire uploads (répertoire courant + uploads)
    const fileStream = fs.createWriteStream(path.join(process.cwd(), 'uploads', 'file.txt'));


    const contentDisposition = req.headers['content-disposition'];
    if (contentDisposition) {
    const filename = contentDisposition.split(';')[1].split('=')[1];
    }
    if (!contentDisposition) {
    res.status(400).send('Il est nécessaire de spécifier la disposition du contenu');
    return;
    }


    req.on('data', (chunk) => {
    // Écriture des données dans le flux d'écriture
    // chunk est un Buffer, il est possible de l'écrire directement dans le flux d'écriture
    fileStream.write(chunk);
    });
    

    req.on('end', () => {
    // Toutes les données ont été reçues
    // Fermeture du flux d'écriture
    fileStream.end();
    res.send('File uploaded successfully');
    });
});


app.get('/download/:filename', (req, res) => {
  // Le nom du fichier à télécharger est spécifié dans le paramètre de requête
  // :filename est un paramètre de requête et sera automatiquement extrait par Express dans req.params['filename'] (ou req.params.filename)
    const file = fs.createReadStream(path.join(process.cwd(), 'uploads', req.params.filename));
    file.pipe(res);
    
    
});

app.post('/upload/:path', (req, res) => {
  const path = decodeURIComponent(req.params.path) || '';
  // '' si le paramètre de requête n'est pas spécifié permettant de téléverser le fichier à la racine du répertoire destiné à recevoir les fichiers
  fs.mkdir(path.join(process.cwd(), 'uploads', path), { recursive: true }, (err) => {
    if (err) {
      res.status(500).send('Erreur lors de la création du répertoire');
    }
  });
});

