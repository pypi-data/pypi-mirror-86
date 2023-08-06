import {LitElement, html, property, customElement, css} from 'lit-element';
import Compressor from 'compressorjs';

@customElement('post-form')
class PostForm extends LitElement {
  @property({type: String}) content;
  @property({type: String}) default = '';
  @property({type: Number, attribute: 'board'}) board;
  @property({type: Boolean, attribute: 'board-editable'}) boardEditable = true;
  @property({type: Function}) afterpost;
  connectedCallback() {
    super.connectedCallback();
    this.content = this.default;
  }
  post() {
    fetch('api/boards/'+this.board, {
      method: 'POST',
      headers: {
        'content-type': 'application/json'
      },
      body: JSON.stringify({
        content: this.content
      })
    }).then(res => {
      this.afterpost()
    });
    this.content = '';
    this.shadowRoot.querySelector('#content').value = '';
    this.requestUpdate();
  }
  static styles = css`
    :host {
      display: grid;
      grid-template-rows: auto 32px;
      align-items: flex-end;
    }
    textarea {
      display: block;
      box-sizing: border-box;
      padding: 8px;
      border: none;
      width: 100%;
      height: 40px;
      outline: none;
      resize: vertical;
    }
    button, label {
      height: 32px;
      width: 56px;
      border: none;
      display: flex;
      justify-content: center;
      align-items: center;
      border-radius: 4px;
      font-size: 0.8rem;
      background: none;
    }
    button svg,
    label svg {
      width: 16px;
      height: 16px;
      display: block;
      fill: #777;
    }
    #toolbox{
      display: flex;
      justify-content: space-between;
      background: #0001;
    }
    label input {
      display: none;
    }
  `;
  loadfile(e) {
    let f = e.target.files[0];
    if (!f) {
      return false;
    }
    new Compressor(f, {
      quality: 0.6,
      mimeType: 'image/jpeg',
      success: (f) => {
        let fr = new FileReader();
        fr.readAsDataURL(f);
        fr.onload = () => {
          this.content += '![]('+fr.result+')';
        }
      }
    });
    e.target.value = '';
  }
  render() {
    return html`
      <textarea
        id='content'
        @input=${(e) => this.content = e.target.value}
        placeholder='メッセージを入力'
      >${this.content}</textarea>
      <div id='toolbox'>
        <div>
          <label>
            <input type='file' @change=${e=>this.loadfile(e)} accept='image/*'/>
            <svg>
              <use xlink:href='static/spritesheet.svg#icon-image'></use>
            </svg>
          </label>
        </div>
        <button @click=${() => this.post()}>
          <svg>
            <use xlink:href='static/spritesheet.svg#icon-send'></use>
          </svg>
        </button>
      </div>
    `;
  }
}
