async function loadRooms() {
  const res = await fetch("/api/rooms");
  const data = await res.json();

  const roomList = document.getElementById("roomList");
  roomList.innerHTML = "";

  data.items.forEach(room => {
    const div = document.createElement("div");
    div.className = "item";
    div.innerHTML = `
      <strong>${room.name}</strong>
      <p>ID: ${room.id} / 수용 인원: ${room.capacity}</p>
      <p>장비: ${room.equipment || "-"}</p>
      <button onclick="deleteRoom(${room.id})">삭제</button>
    `;
    roomList.appendChild(div);
  });
}

async function createRoom() {
  const body = {
    name: document.getElementById("roomName").value,
    capacity: Number(document.getElementById("roomCapacity").value),
    equipment: document.getElementById("roomEquipment").value
  };

  const res = await fetch("/api/rooms", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body)
  });

  if (!res.ok) {
    alert("세미나룸 등록 실패");
    return;
  }

  await loadRooms();
}

async function deleteRoom(id) {
  if (!confirm("삭제하시겠습니까?")) return;

  await fetch(`/api/rooms/${id}`, {
    method: "DELETE"
  });

  await loadRooms();
  await loadReservations();
}

async function loadReservations() {
  const roomId = document.getElementById("filterRoomId").value;
  const date = document.getElementById("filterDate").value;

  let url = "/api/reservations";
  const params = new URLSearchParams();

  if (roomId) params.append("room_id", roomId);
  if (date) params.append("date", date);

  if (params.toString()) {
    url += `?${params.toString()}`;
  }

  const res = await fetch(url);
  const data = await res.json();

  const reservationList = document.getElementById("reservationList");
  reservationList.innerHTML = "";

  data.items.forEach(reservation => {
    const div = document.createElement("div");
    div.className = "item";
    div.innerHTML = `
      <strong>${reservation.room_name}</strong>
      <p>예약자: ${reservation.user_name} (${reservation.user_email})</p>
      <p>날짜: ${reservation.date}</p>
      <p>시간: ${reservation.start_time} ~ ${reservation.end_time}</p>
      <p>목적: ${reservation.purpose || "-"}</p>
      <button onclick="deleteReservation(${reservation.id})">예약 취소</button>
    `;
    reservationList.appendChild(div);
  });
}

async function createReservation() {
  const body = {
    room_id: Number(document.getElementById("resRoomId").value),
    user_name: document.getElementById("resUserName").value,
    user_email: document.getElementById("resUserEmail").value,
    date: document.getElementById("resDate").value,
    start_time: document.getElementById("resStartTime").value + ":00",
    end_time: document.getElementById("resEndTime").value + ":00",
    purpose: document.getElementById("resPurpose").value
  };

  const res = await fetch("/api/reservations", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body)
  });

  if (!res.ok) {
    const error = await res.json();
    alert(error.message || "예약 실패");
    return;
  }

  await loadReservations();
}

async function deleteReservation(id) {
  if (!confirm("예약을 취소하시겠습니까?")) return;

  await fetch(`/api/reservations/${id}`, {
    method: "DELETE"
  });

  await loadReservations();
}

loadRooms();
loadReservations();
