<template>
  <div id="app">
    <div class="container grid-960">
      <h2>Headphone Recommender</h2>
      <div class="toast toast-error" id="error-toast" style="display:none">
        <button class="btn btn-clear float-right" v-on:click="closeErr"></button>
        Error <span id="error-msg"></span>     :(
      </div>
      <div class="columns">
        <div class="column">
          <form v-on:submit.prevent="submit">
            <!-- form input control -->
            <div class="form-group">
              <label class="form-label" for="input-file">MP3</label>
              <input class="form-input" type="file" id="input-file" accept=".mp3" required/>
            </div>
            <div class="form-group" v-for="option in options" v-bind:class="{hide: option.hide}" v-bind:id="option.wrapper">
              <label class="form-label" v-bind:for="option.id">{{ option.label }}</label>
              <select class="form-select" v-bind:id="option.id" v-on:input="updateForm">
                <option v-for="value in option.values">{{ value }}</option>
              </select>
            </div>
            <div style="margin-top: 20px" >
              <button class="btn btn-primary input-group-btn" type="button" style="display:none" v-on:click="showModal">Show Results</button>
              <button class="btn btn-primary input-group-btn" type="submit" id="submit">Submit</button>
            </div>
          </form>
        </div>
        <div class="divider-vert"></div>
        <div class="column">
          <h4>{{ help.title }}</h4>
          <ol>
            <li v-for="val in help.list">{{ val }}</li>
          </ol>
          <div class="divider text-center" data-content="INFORMATION"></div>
          <div class="column" v-for="(value, key) in info" v-bind:id="key" v-bind:class="{hide: value.hide}">
            <h4>{{ value.title }}</h4>
            <ol>
              <li v-for="item in value.list">{{ item }}</li>
            </ol>
          </div>
        </div>
      </div>
      <div class="modal" id="response-modal">
        <div class="modal-overlay" v-on:click="closeModal"></div>
        <div class="modal-container">
          <div class="modal-header">
            <button class="btn btn-clear float-right modal-close"></button>
            <div class="modal-title"><b>Analysis Results</b></div>
          </div>
          <div class="modal-body">
            <div id="freqdata" class="content">
              <p>Frequency Response Plot</p>
              <img id="freqPlot" width="500px">
            </div>
            <div class="content">
              <p>Analyzed frequency response type most closely matched: <b id="response"></b>.</p>
              <p>Recommended Headphones: </p>
            </div>
            <div id="headphonetable"> </div>
          </div>
          <div class="modal-footer">
            <a href="javascript:void(0)" class="btn btn-primary modal-close">close</a>
          </div>
        </div>
      </div>
    </div>
    <vue-progress-bar></vue-progress-bar>
  </div>
</template>

<script>
import $ from 'jquery'
import axios from 'axios'

export default {
  name: 'app',
  mounted () {
    this.$Progress.finish();
  },
  created () {
    this.$Progress.start();
  },
  data () {
    return {
      help: {
        title: 'How it works',
        list: [
          'Input an mp3 file for a song you like',
          'The file is analyzed for it\'s sound signature',
          'A headphone is recommended based on your preferences',
          'Note: Heroku only has 512 mb of ram, which is not enough to perform fft on large file sizes. Please keep song durations to under 4:15.'
        ]
      },
      options: [
        {
          label: 'Style',
          id: 'type',
          values: [
            'Over Ear',
            'On Ear',
            'In Ear Monitor'
          ],
          hide: false
        },
        {
          label: 'Portability',
          id: 'portability',
          wrapper: 'portability-wrapper',
          values: [
            'Portable',
            'Not Portable'
          ],
          hide: false
        },
        {
          label: 'Fit',
          id: 'fit',
          wrapper: 'fit-wrapper',
          values: [
            'Over The Ear',
            'Straight Down'
          ],
          hide: true
        },
        {
          label: 'Soundstage',
          id: 'soundstage',
          wrapper: 'soundstage-wrapper',
          values: [
            'Open Back',
            'Closed Back'
          ],
          hide: true
        }
      ],
      info: {
        overearhelp: {
          title: 'Portability',
          list: [
            'Non-Portable Headphones can be used with a DAC/AMP.',
            'Some of these may rely on a DAC/AMP to bring the full potential out of the headphones.',
            'However, non-portable headphones are better suited for those on the go.'
          ],
          hide: false
        },       
        onearhelp: {
          title: 'What is Soundstage?',
          list: [
            'Soundstage is the quality that lets you determine the spatial location of instruments in the music (i.e, 3-D location)',
            'Open-backed headphones tend to leak sound outside, but have far superior soundstage.',
            'Closed-back headphones don\'t leak sound, making them preferable for workplaces.'
          ],
          hide: true
        },
        iemhelp: {
          title: 'IEM Fit Types',
          list: [
            'Over the Ear IEMS are looped behind and over the ear before being inserted in the ear.',
            'They typically prevent much microphonics, the noise that travels up the wire when you bump into the it.',
            'Straight down is how many IEMS are worn, including the Apple Earpods.',
            'They typically suffer from worse microphonics.'
          ],
          hide: true
        }
      }
    }
  },
  methods: {
    makeTable: function (data) {
      let table = '<table class="table table-striped table-hover">';
      table += '<thead><tr><th>Estimated Price</th>';
      table += '<th>Headphone</th></tr></thead><tbody>';

      let headphones = [];
      $.each(data, function (name, price) {
        let h = Object();
        h.name = name;
        h.price = price;
        headphones.push(h);
      });
      headphones.sort(function (a, b) {
        return parseInt(a.price) - parseInt(b.price);
      });
      for (let i = 0; i < headphones.length; ++i) {
        let price = headphones[i].price;
        let name = headphones[i].name;
        let url = 'https://www.amazon.com/s/field-keywords=' + encodeURI(name);
        let row = `<tr><td>$${price}</td><td><a href=${url} target="_blank">${name}</a></td><tr>`;
        table += row;
      }
      table += '</tbody></table>';
      return table;
    },
    updateForm: function () {
      let option = $('#type option:selected').text();

      if (option === 'On Ear') {
        $('#portability-wrapper, #fit-wrapper, #overearhelp, #iemhelp').addClass('hide');
        $('#soundstage-wrapper, #onearhelp').removeClass('hide');

      } else if (option === 'In Ear Monitor') {
        $('#fit-wrapper, #iemhelp').removeClass('hide');
        $('#portability-wrapper, #soundstage-wrapper, #onearhelp, #overearhelp').addClass('hide');
      } else { //over ear
        if ($('#portability option:selected').text() === 'Not Portable') {
          $('#soundstage-wrapper').removeClass('hide');
        } else {
          $('#soundstage-wrapper').addClass('hide');
        }
        $('#onearhelp, #iemhelp, #fit-wrapper').addClass('hide');
        $('#overearhelp, #portability-wrapper').removeClass('hide');
      }
    },
    showErr: function () {
      $('#error-toast').show();
      $('#submit').removeClass('loading');
    },
    closeErr: function () {
      $('#error-toast').hide();
    },
    validMp3Input: function () {
      // verify if .mp3 file
      let mp3 = $('#input-file')[0].files[0];
      if (!mp3.name.endsWith('.mp3')) {
        $('#error-msg').text('Invalid file, please select an .mp3');
        this.showErr();
        return false;
      }

      // verify if .mp3 is under 20MB
      if (mp3.size > 20971520) {
        $('#error-msg').text('File too large, please select a smaller .mp3 under 20MB');
        this.showErr();
        return false;
      }

      return true;
    },
    submit: function () {
      $('#submit').addClass('loading');
      $('#error-toast').hide(); // hide error on resubmit

      if (this.validMp3Input()) {
        this.submitData();
      }
    },
    submitData: function () {
      let mp3 = $('#input-file')[0].files[0];

      //Reset Form
      $('#headphonetable').empty();
      $('.modal-open').hide();
      // create form data
      const data = new FormData();
      data.append('type', $('#type option:selected').text());

      if ($('#portability').is(':visible')) {
        data.append('opt1', $('#portability option:selected').text());
      }

      if ($('#fit').is(':visible')) {
        data.append('opt1', $('#fit option:selected').text());
      }

      if ($('#soundstage').is(':visible')) {
        data.append('opt2', $('#soundstage option:selected').text());
      }

      data.append('price', $('#price option:selected').text());
      data.append('file', mp3);

      this.$Progress.start();

      axios.post('/upload', data) // eslint-disable-line no-undef
        .then((response) => {
          $('#response').text(response.data.signature);
          $('#freqPlot').attr('src', response.data.plotpath);
          $('#response-modal').addClass('active');
          $('#submit').removeClass('loading');
          $('.modal-open').show();
          console.log(response.data.headphones); // eslint-disable-line no-console

          let table = this.makeTable(response.data.headphones);
          $(table).appendTo('#headphonetable');

          this.$Progress.finish();
        })
        .catch((error) => {
          let msg = error.response.status;
          if (error.response.data.message){
            msg += ': ' + error.response.data.message
          }
          $('#error-msg').text(msg);
          this.showErr();

          this.$Progress.fail();
        });
    },
    closeModal: function () {
      $('#response-modal').removeClass('active');
    },
    showModal: function () {
      $('#response-modal').addClass('active');
    }
  }
}
</script>

<style>
h2 {
  margin-top:10%;
}
</style>
