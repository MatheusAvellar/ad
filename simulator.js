class Simulator {
  constructor() {
    // Lista de eventos
    this.events = [];
    // Variáveis de estado
    this.state = {
      // O tempo atual da simulação
      time: 0,
      // Número de clientes no sistema
      N: 0,
    };
  }

  init() {
    console.log("[init]");
    // Inicializa variáveis de estado
    
    // Inicializa lista de eventos
    this.addEvent(this.createEvent("arrival", 0.4));
    // Começa o simulador
    this.run();
  }

  run() {
    console.log("[run]");
    // Enquanto a lista de eventos não estiver vazia
    let i = 10;
    while(this.events.length > 0 && i-->0) {
      console.log("Lista de eventos:",JSON.stringify(this.events));
      // Remove primeiro evento da lista
      const event = this.events.shift();
      // Trata o evento
      this.eventHandler(event);
    }
  }

  eventHandler(event) {
    console.log("[eventHandler]", event);
    this.state.time = event.time;
    this.state.N++;
    const departure_time = event.time + this.getRandomDuration("departure");
    const departure = this.createEvent("departure", departure_time);
    const arrival_time = event.time + this.getRandomDuration("arrival");
    const arrival = this.createEvent("arrival", arrival_time);

    if(arrival_time < departure_time) {
      this.addEvent(arrival);
      this.addEvent(departure);
    } else {
      this.addEvent(departure);
      this.addEvent(arrival);
    }
  }

  getRandomDuration(type) {
    console.log("[getRandomDuration]", type);
    switch(type) {
      case "arrival":
        return (this.randomIntRange(1,100))/100;
      case "departure":
        return (this.randomIntRange(1,100))/100;
      default:
        console.warn(`[getRandomDuration] Unknown type '${type}'`);
        return 0;
    }
  }
  randomIntRange(min, max) {
    // [Ref] https://stackoverflow.com/a/1527820/4824627
    console.log("[randomIntRange]", min, max);
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  createEvent(type, time) {
    console.log("[createEvent]", type, time);
    return {
      type: type, time: time
    };
  }
  addEvent(event) {
    console.log("[addEvent]", event);
    this.events.push(event);
  }
}