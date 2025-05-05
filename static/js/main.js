document.getElementById("moodForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const sentence = document.getElementById("dailySentence").value;
  const mood = parseInt(document.getElementById("moodSelect").value);

  // 🌱 API'ye veri gönder
  await fetch("http://localhost:8000/mood", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: "deneme", // bunu ileride kullanıcıya göre dinamik yaparsın
      sentence: sentence,
      mood: mood,
      date: new Date().toISOString().slice(0, 10),
    }),
  });

  // 🌼 Çiçeği görsel olarak ekle
  const flower = document.createElement("img");
  flower.src = `assets/flower${mood}.svg`;
  flower.className = "flower";
  document.getElementById("garden-view").appendChild(flower);

  // Formu temizle
  document.getElementById("dailySentence").value = "";
  document.getElementById("moodSelect").selectedIndex = 0;
});

// 🕰️ Sayfa yüklendiğinde geçmiş mood'ları getir
window.addEventListener("DOMContentLoaded", async () => {
  const response = await fetch("http://localhost:8000/mood-history/deneme");
  const moodHistory = await response.json();

  moodHistory.forEach((entry) => {
    const flower = document.createElement("img");
    flower.src = `assets/flower${entry.mood}.svg`;
    flower.className = "flower";
    document.getElementById("garden-view").appendChild(flower);
  });
});
