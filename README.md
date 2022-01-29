# Context
Our model predict the time to sell a product on Label Emmaüs marketplace.
It's a standard classification problem with 3 classes.
We will use log loss metric during train, and predict a probability for each class during a prediction.




# Product deployment
clone repository
```shellscript
cd  allisone
```
make shell script executable
```shellscript
chmod u+x install.sh
```

create virtual env named allisone and install
dependencies
```shellscript
./install.sh
```

activate your venv
```shellscript
source allisone/bin/activate
```