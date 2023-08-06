import {LitElement, customElement, property, html, css} from 'lit-element';

@customElement('board-form')
class BoardForm extends LitElement {
  @property({type: Array}) groups = [];
  async connectedCallback() {
    super.connectedCallback();
    fetch('api/groups').then(res => res.json()).then(res => {
      this.groups = res;
      console.log(this.groups);
      this.requestUpdate();
    });
  }
  static styles = css`
    :host{
      displat: block;
    }
    form {
      display: block;
      padding: 24px;
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 0 8px #0004;
    }
    textarea {
      height: 1em;
      min-height: 1em;
    }
  `;
  render() {
    return html`
      <form id='board-form'>
        <input type='text' name='subject' placeholder='スレタイ'/>
        <label><input type='checkbox' name='private'/> 非公開ボード</label>
        <textarea name='description' placeholder='スレッド詳細'></textarea>
        <select name='group'>
        ${ this.groups.map(group => html`
          <option value='${group.id}'>${group.name}</option>
          `) }
        </select>
        <button type='button' id='create_btn'>作成</button>
      </form>
    `;
  }
}
