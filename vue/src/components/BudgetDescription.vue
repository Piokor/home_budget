<template>  
  <div>
    <div class="text-h3">
      Budget: {{budget.title}}
    </div>

    <div class="text-caption" v-if="budget.owner_name">
      Owner: {{budget.owner_name}}
    </div>

    <div class="text-subtitle-2">
      {{budget.description}}
    </div>
  </div>
</template>


<script>
export default {
  props: ["budget"],

  methods: {

  }
};
</script>