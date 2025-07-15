package test;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.util.Set;

import org.designwizard.api.DesignWizard;
import org.designwizard.design.ClassNode;
import org.designwizard.design.PackageNode;
import org.junit.Test;

public class DesignTest {
    @Test
    public void testStrategyDoesNotHoldReferencesToContext() throws Exception {
        // Always instantiate DesignWizard exactly like this
        DesignWizard dw = new DesignWizard("bin");

        // Get the Strategy classes
        ClassNode strategyA = dw.getClass("com.cnblog.clarck.ConcreateStrategyA");
        ClassNode strategyB = dw.getClass("com.cnblog.clarck.ConcreateStrategyB");
        ClassNode strategyC = dw.getClass("com.cnblog.clarck.ConcreateStrategyC");

        // Get the Context class
        ClassNode context = dw.getClass("com.cnblog.clarck.Context");

        // Get the classes referenced by the Strategy classes
        Set<ClassNode> strategyACalleeClasses = strategyA.getCalleeClasses();
        Set<ClassNode> strategyBCalleeClasses = strategyB.getCalleeClasses();
        Set<ClassNode> strategyCCalleeClasses = strategyC.getCalleeClasses();

        // Assert that the Strategy classes do not reference the Context class
        assertFalse(strategyACalleeClasses.contains(context));
        assertFalse(strategyBCalleeClasses.contains(context));
        assertFalse(strategyCCalleeClasses.contains(context));
    }
}