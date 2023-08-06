import { TextLikeInput, TextLikeInputView } from "./text_like_input";
import { input } from "../../core/dom";
import { bk_input } from "../../styles/widgets/inputs";
export class TextInputView extends TextLikeInputView {
    _render_input() {
        this.input_el = input({ type: "text", class: bk_input });
    }
}
TextInputView.__name__ = "TextInputView";
export class TextInput extends TextLikeInput {
    constructor(attrs) {
        super(attrs);
    }
    static init_TextInput() {
        this.prototype.default_view = TextInputView;
    }
}
TextInput.__name__ = "TextInput";
TextInput.init_TextInput();
//# sourceMappingURL=text_input.js.map