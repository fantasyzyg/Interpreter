package ast;

import java.util.ArrayList;
import java.util.List;

public class Compound extends AST{
    private List<AST> children;

    public Compound() {
        this.children = new ArrayList<>();
    }

    public List<AST> getChildren() {
        return children;
    }
}
