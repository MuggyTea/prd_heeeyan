<template>
  <v-app>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>Heeeyan</span>
        <span class="font-weight-light">SEO DESIGN</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn flat href="https://github.com/vuetifyjs/vuetify/releases/latest" target="_blank">
        <span class="mr-2">Latest Release</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-toolbar>

    <v-content>
      <FormText />
    </v-content>
  </v-app>
</template>

<script>
import FormText from './components/FormText'

export default {
  name: 'App',
  components: {
    FormText
  },
  data () {
    return {
      //
    }
  }
}
</script>
