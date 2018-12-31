class WebSocketService {
  static instance = null;
  callbacks = {};

  static getInstance() {
    if (!WebSocketService.instance) {
      WebSocketService.instance = new WebSocketService();
    }
    return WebSocketService.instance;
  }

  constructor() {
    this.socketRef = null;
  }

  connect() {
    const path = "ws://localhost:8000/ws/ohqueue";
    this.socketRef = new WebSocket(path);
    this.socketRef.onopen = () => {
    };
    this.socketRef.onmessage = e => {
      this.callbacks['set'](JSON.parse(e.data))
    };

    this.socketRef.onerror = e => {
      console.log(e.message);
    };
    this.socketRef.onclose = () => {
      this.connect();
    };
  }

  addCallbacks(updateCallBack) {
    this.callbacks['set'] = updateCallBack;
  }
  

  state() {
    return this.socketRef.readyState;
  }

   waitForSocketConnection(callback){
    const socket = this.socketRef;
    const recursion = this.waitForSocketConnection;
    setTimeout(
      function () {
        if (socket.readyState === 1) {
          console.log("Connection is made")
          if(callback != null){
            callback();
          }
          return;

        } else {
          console.log("wait for connection...")
          recursion(callback);
        }
      }, 1); 
  }

}

const WebSocketInstance = WebSocketService.getInstance();

export default WebSocketInstance;
