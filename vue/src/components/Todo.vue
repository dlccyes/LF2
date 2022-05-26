<script>
let id = 3;
let sample = {};
for(let i=0; i<id; i++){
  sample[i] = "sample " + i;
}

export default {
  data() {
    return {
      newTodo: '',
      todos: sample,
    }
  },
  methods: {
    addTodo() {
      this.todos[id++] = this.newTodo
    },
    removeTodo(id) {
      console.log(id)
      delete(this.todos[id])
    }
  }
}
</script>
<template>
  <form @submit.prevent="addTodo">
    <input v-model="newTodo">
    <button>Add Todo</button>    
  </form>
  <ul>
    <li v-for="(text, id) in todos" :key="id">
      {{text}} {{id}}
      <button @click="removeTodo(id)">X</button>
    </li>
  </ul>
</template>