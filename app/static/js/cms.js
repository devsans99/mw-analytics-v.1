// CMS-only Alpine components. Loaded after Quill, before Alpine.
document.addEventListener("alpine:init", () => {
  // Rich text editor bound to a hidden <textarea x-ref="input">.
  Alpine.data("richEditor", () => ({
    quill: null,
    init() {
      const input = this.$refs.input;
      this.quill = new Quill(this.$refs.editor, {
        theme: "snow",
        modules: {
          toolbar: [
            [{ header: [2, 3, false] }],
            ["bold", "italic", "underline"],
            [{ list: "ordered" }, { list: "bullet" }],
            ["blockquote", "link"],
            ["clean"],
          ],
        },
      });
      if (input.value) {
        this.quill.clipboard.dangerouslyPasteHTML(input.value);
      }
      this.quill.on("text-change", () => {
        input.value = this.quill.getSemanticHTML();
      });
    },
  }));
});
