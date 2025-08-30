
const firebaseConfig = {
  apiKey: "AIzaSyATMosG7lqdXI5t5zsBnkVDYYdP3Q3CXyg",
  authDomain: "reactgym-3a6a9.firebaseapp.com",
  projectId: "reactgym-3a6a9",
  storageBucket: "reactgym-3a6a9.firebasestorage.app",
  messagingSenderId: "137596921738",
  appId: "1:137596921738:web:acc821a32632c983ff4a73",
  measurementId: "G-6M4E5ST4L2"
};


firebase.initializeApp(firebaseConfig);


const db = firebase.firestore();
const Timestamp = firebase.firestore.Timestamp;


const messagesList = document.getElementById('messages-list');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');


const sender = "UserA";
const friendName = "UserB";


const chattersQuery1 = `${sender}xx${friendName}`;
const chattersQuery2 = `${friendName}xx${sender}`;


const queryResult = db.collection('Chats').where('chatters', '==', chattersQuery1);
const queryResult2 = db.collection('Chats').where('chatters', '==', chattersQuery2);

#fetch tin nhắn khi tải lên
const loadInitialMessages = async () => {
    try {
        const querySnapshot = await queryResult.get();
        const querySnapshot2 = await queryResult2.get();

        if (!querySnapshot.empty) {
            renderMessages(querySnapshot.docs[0].data().conversation);
        } else if (!querySnapshot2.empty) {
            renderMessages(querySnapshot2.docs[0].data().conversation);
        }
    } catch (error) {
        console.error("Error loading initial messages:", error);
    }
};


queryResult.onSnapshot((snapshot) => {
    if (!snapshot.empty) {
        const conversation = snapshot.docs[0].data().conversation;
        renderMessages(conversation);
    } else {

        messagesList.innerHTML = '';
    }
});


queryResult2.onSnapshot((snapshot) => {
    if (!snapshot.empty) {
        const conversation = snapshot.docs[0].data().conversation;
        renderMessages(conversation);
    } else {

        messagesList.innerHTML = '';
    }
});
const renderMessages = (conversation) => {
    messagesList.innerHTML = '';


    conversation.sort((a, b) => a.timestamp?.seconds - b.timestamp?.seconds);
    conversation.forEach(msg => {
        const messageDiv = document.createElement('div');
        messageDiv.textContent = msg.message;
        messageDiv.classList.add('message');
        if (msg.sender === sender) {
            messageDiv.classList.add('sent');
        } else {
            messageDiv.classList.add('received');
        }
        messagesList.appendChild(messageDiv);
    });

    messagesList.scrollTop = messagesList.scrollHeight;
};


const handleSubmit = async () => {
    const messageText = messageInput.value.trim();
    if (messageText === '') return;

    try {
        const newMessage = {
            message: messageText,
            sender: sender,
            timestamp: Timestamp.now()
        };


        const snapshot1 = await queryResult.get();
        const snapshot2 = await queryResult2.get();

        if (!snapshot1.empty) {

            const docRef = snapshot1.docs[0].ref;

            await docRef.update({
                conversation: firebase.firestore.FieldValue.arrayUnion(newMessage)
            });
        } else if (!snapshot2.empty) {

            const docRef = snapshot2.docs[0].ref;

            await docRef.update({
                conversation: firebase.firestore.FieldValue.arrayUnion(newMessage)
            });
        } else {

            await db.collection('Chats').add({
                chatters: chattersQuery1,
                conversation: [newMessage]
            });
        }
        messageInput.value = '';
    } catch (error) {
        console.error("Lỗi khi gửi tin nhắn: ", error);
        alert("Không thể gửi tin nhắn.");
    }
};


sendButton.addEventListener('click', handleSubmit);


messageInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        handleSubmit();
    }
});

loadInitialMessages()

