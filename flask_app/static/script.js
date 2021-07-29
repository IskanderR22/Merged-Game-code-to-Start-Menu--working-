console.log('hello there');

var form_data = [];

var classes = {
    "Wizard": {
        "health": 100,
        "strength": 2, 
        "magic": 15,
        "durability": 5,
        "speed": 5,
    },
    "Ranger": {
        "health": 100,
        "strength": 8, 
        "magic": 8,
        "durability": 8,
        "speed": 10,
    },
    "Guardian": {
        "health": 200,
        "strength": 15, 
        "magic": 11,
        "durability": 10,
        "speed": 2,
    }
};

function testFunc(element) {
    console.log("TESTESTESTESTESTESTESTED!!!!!!!!!!")
}

function createPlayer(element) {
    var className = element.getAttribute("value");
    var classData = {
        ...classes[className],
        "class": className,
        "money": 50
    };
    fetch("http://localhost:5000/api/pcs/create", {
        method: 'POST',
        body: JSON.stringify(classData),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data =>  {
        console.log(data);
    })
}

function redirect(){
    location.href = "/start_menu"
}



function passClass(form_data) {
    if (form_data['class'] == "Wizard") {
        // user_id
        // health:100
        // strength: 2
        // magic: 15
        // durability: 5
        // speed: 5
        // money: 50
        let health = 100;
        let strength = 2;
        let magic = 15;
        console.log(100);
        location.replace(`http://localhost:5000/create/wizard/${logged_user.username}/${health}`);
    } else if (form_data['class'] == "Ranger") {
        // user_id
        // health:100
        // strength: 8
        // magic: 8
        // durability: 8
        // speed: 10
        // money: 50
    } else if (form_data['class'] == "Guardian") {
        // user_id
        // health:200
        // strength: 15
        // magic: 1
        // durability: 10
        // speed: 2
        // money: 50
    }
}


