function searchEnter(event)
{
    document.getElementById("searchbar").placeholder = "Where are we going next?";
    return isNumberKey(event);
}

function addLocation(locationName)
{
    var ul = document.getElementById("locationList");
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(locationName));
    ul.appendChild(li);
}