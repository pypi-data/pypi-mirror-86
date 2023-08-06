import {LitElement, customElement, html, css, property} from 'lit-element';

@customElement('board-create-button')
class BoardCreateButton extends LitElement {
  @property({type: Object}) group = {};
  @property({type: Function}) addColumn;
  static styles = css`
    :host{
      display: inline-block;
      position: relative;
      width: 24px;
      height: 24px;
      border-radius: 8px;
      background: #0002;
    }
    :host(:hover){
      background: #0004;
    }
    :host(:active){
      background: #0007;
    }
    input[type='checkbox'] {
      display: none;
    }
    #plus{
      position: absolute;
      display: block;
      width: 12px;
      height: 12px;
      padding: 6px;
      top: 0;
      transition: all.2s;
    }
    #plus::before,
    #plus::after{
      content: '';
      display: block;
      width: 12px;
      position: absolute;
      height: 2px;
      background: #fff;
      top: 11px;
      left: 6px;
      transform-origin: center;
    }
    #plus::before{
      transform: rotate(90deg);
    }
    board-create-form{
      position: absolute;
      left: 0px;
      top: 0;
      opacity: 0;
      transition: all.2s;
      pointer-events: none;
    }
    #toggle:checked~board-create-form{
      display: block;
      opacity: 1;
      left: 32px;
      pointer-events: all;
    }
    #toggle:checked~#plus {
      transform: rotate(45deg);
    }
  `;
  _addColumn(a) {
    this.shadowRoot.querySelector('#toggle').checked = false;
    this.addColumn(a);
  }
  render() {
    return html`
      <input type='checkbox' id='toggle' />
      <label id='plus' for='toggle'></label>
      <board-create-form .group=${this.group} .addColumn=${a => this._addColumn(a)}></board-create-form>
    `;
  }
}
