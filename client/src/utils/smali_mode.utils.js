export function installSmaliMode(Editor) {
    Editor.defineMode("smali", function () {
        return {
            token: function(stream, state) {

                const nextChar = stream.next()

                if (nextChar === "#") { stream.skipToEnd(); return "comment" }

                if (nextChar === "." && stream.match(/(source|line|field|annotation|super|class|method|end|implements|registers)(\s(method|annotation|runtime|field|system))?/))
                {
                    return "def"
                }

                if (nextChar === "L" && stream.match(/[^\(;:\n]*;/))
                {
                    return "type";
                }

                if (nextChar === "\"")
                {
                    stream.skipTo('"')
                    return "string";
                }

                if (nextChar.match(/v|p/) && stream.match(/\d/))
                {
                    return "variable";
                }

                if ((nextChar==="0" && stream.match(/x[0-9a-fA-F]+/)) || nextChar.match(/^\d+$/))
                {
                    return "number";
                }

                if (nextChar.match(/\s/) && stream.match(/(abstract|final|public|private|interface|static|protected|synthetic|constructor)(?=\s)/))
                {
                    return "attribute";
                }

                if (nextChar.match(/\</) && stream.match(/init\>/))
                {
                    return "qualifier"
                }

                if (stream.match(/throw(?=(\s))/))
                {
                    return "error"
                }

            }
          };
      });

      Editor.defineMIME("text/smali", "smali");
}