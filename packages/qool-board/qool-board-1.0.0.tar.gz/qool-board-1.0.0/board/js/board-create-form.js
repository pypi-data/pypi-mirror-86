import {LitElement, customElement, property, html, css} from 'lit-element';

@customElement('board-create-form')
class BoardCreateForm extends LitElement {
  @property({type: Object}) group = {};
  @property({type: Function}) addColumn;
  static styles = css`
    :host {
      display: block;
      background: #fff;
      box-shadow: 0 0 8px #0003;
      padding: 16px;
      width: 200px;
    }
    #subject{
      height: 32px;
      line-height: 32px;
      width: 100%;
      box-sizing: border-box;
      padding: 0 8px;
      border: 0;
      border-bottom: 2px solid #333c5e;
      outline: none;
    }
    #description {
      border: 0;
      box-sizing: border-box;
      width: 100%;
      padding: 8px;
      border: 1px solid #333c5e;
      outline: none;
      resize: vertical;
    }
    #private {
      display: flex;
      align-items: center;
      font-size: 0.7rem;
    }
    #private input{
    }
    #submit{
      display: flex;
      justify-content: flex-end;
    }
    dl{
      margin: 0;
    }
    dd {
      margin: 0 0 8px;
    }
    dt {
      margin: 0 0 4px;
      font-size: 0.7rem;
      font-weight: bold;
    }
    button {
      height: 32px;
      line-height: 32px;
      border-radius: 16px;
      background: #333c5e;
      color: #fff;
      font-size: 0.7rem;
      font-weight: bold;
      padding: 0 16px;
      border: none;
      outline: none;
    }
  `;
  submitForm(e) {
    e.preventDefault();
    const form = new FormData(e.target);
    fetch('api/boards', {
      method: 'POST',
      body: form
    }).then(res => res.json()).then(res => {
      this.addColumn(res._id);
    });
    return false;
  }
  render() {
    return html`
      <form @submit=${e => this.submitForm(e)}>
        <input type='hidden' name='group' value=${this.group._id} />
        <dl>
          <dt>ボードタイトル</dt>
          <dd>
            <input type='text' name='subject' id='subject' placeholder='ボードタイトル' />
          </dd>
          <dt>トピック</dt>
          <dd>
            <textarea name='description' id='description' placeholder='トピック'></textarea>
          </dd>
          <!--
          <dd>
            <label id='private'>
              <input type='checkbox' name='private'> 参加者以外に非公開にする
            </label>
          </dd>
          -->
        </dl>
        <div id='submit'>
          <button>ボードを作成</button>
        <div>
      </form>
    `;
  }
}
