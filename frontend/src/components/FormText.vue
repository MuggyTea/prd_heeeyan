<template>
  <v-card max-width="70%" class="mx-auto">
    <v-card-title class="accent">投稿フォーム</v-card-title>
    <v-form>
      <v-expansion-panel expand v-model="isExpand">
        <v-expansion-panel-content>
          <template v-slot:header>
            <div>{{ expandMessage }}</div>
          </template>
          <v-card-text>
            <v-textarea v-model="beforeText" label="記事を書いてね"></v-textarea>
          </v-card-text>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-btn class="primary" @click="submit">投稿</v-btn>
      <v-btn class="accent" @click="clear">クリア</v-btn>
    </v-form>
    <v-list two-line>
      <template v-for="(aftertext, index) in afterTexts">
        <v-list-tile :key="index">
          <v-list-tile-content>
            <v-list-tile-title id="copyTarget" v-html="aftertext.city_text"></v-list-tile-title>
            <v-btn class="primary" @click="copyText">コピー</v-btn>
          </v-list-tile-content>
        </v-list-tile>
      </template>
    </v-list>
  </v-card>
</template>

<script>
import axios from 'axios'
export default{
  data: function () {
    return {
      isExpand: [],
      beforeText: '',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8',
        'Access-Control-Allow-Origin': '*'
      },
      afterTexts: [],
      cityText: ''
    }
  },
  computed: {
    expandMessage () {
      // パネルが開いてたらtrue
      return this.isExpand[0] ? '閉じる' : '開く'
    }
  },
  methods: {
    submit () {
      // POST送信する
      axios.post(
        'http://127.0.0.1:5000/',
        {
          beforeText: this.beforeText
        }
      )
      // 送信完了
        .then((res) => {
          console.log(res)
          console.log(res.data.after_text)
          this.afterTexts = res.data.after_text
        })
        .catch(error => {
          console.log(error)
        })
    },
    clear () {
    //   this.$v.$reset()
      this.beforeText = ''
    },
    copyText () {
      var copyText = document.querySelector('#copyTarget')
      console.log(copyText)
      console.log(this.document)
      var range = document.createRange()
      console.log(range)
      range.selectNodeContents(copyText)
      var selection = window.getSelection()
      console.log(selection)
      selection.removeAllRanges()
      selection.addRange(range)
      if (document.execCommand('copy')) {
        console.log('コピーしました')
        console.log(copyText)
      } else {
        console.log('失敗したよ')
        console.log(copyText)
        console.log(range)
        console.log(selection)
      }
    }
  }
}

</script>
