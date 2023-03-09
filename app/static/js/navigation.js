const navigation = document.getElementById("navigation");
const collapse = document.getElementById("collapse");

collapse.addEventListener("click", () => {
  navigation.classList.toggle("collapsed");
  document.cookie = `collapsed=${
    navigation.classList.contains("collapsed") ? "true" : "false"
  }`;
});
