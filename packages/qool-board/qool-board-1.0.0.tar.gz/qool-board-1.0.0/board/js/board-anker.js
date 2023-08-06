import {LitElement, customElement, property, html} from 'lit-element';

@customElement('board-anker')
class BoardAnker extends LitElement {
  @property({type: String, attribute: 'href'}) href; 
  constructor() {
    super();
    this.addEventListener('click', () => {
      let link = this.href;
      docuemnt.querySelector(link).scrollIntoView();
    });
  }
  render() {
    return html`<slot></slot>`;
  }
}
