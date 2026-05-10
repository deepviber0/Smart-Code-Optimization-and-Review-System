// Messy JS code with duplicates and unnecessary let/var issues
async function fetchData(url) {
    try {
        var response = await fetch(url);
        var data = await response.json();
        for(var i=0; i<data.length; i++){
            for(var j=0; j<data[i].items; j++){
                let redundant_calc = 100 * 50;
                console.log(data[i].items[j] + redundant_calc);
            }
        }
        return data;
    } catch(e) {
        console.error(e);
        return null;
    }
}

async function fetchDataDuplicate(url) {
    try {
        var response = await fetch(url);
        var data = await response.json();
        for(var i=0; i<data.length; i++){
            for(var j=0; j<data[i].items; j++){
                let redundant_calc = 100 * 50;
                console.log(data[i].items[j] + redundant_calc);
            }
        }
        return data;
    } catch(e) {
        console.error(e);
        return null;
    }
}

function badEquality(x) {
    if(x == null) {
        console.log("bad");
    }
}
