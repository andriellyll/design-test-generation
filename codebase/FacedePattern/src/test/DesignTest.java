package test;

import static org.junit.Assert.*;
import org.junit.Test;
import org.junit.Ignore;

import org.junit.Before;

import java.util.HashSet;
import java.util.Set;

import org.designwizard.api.DesignWizard;
import org.designwizard.design.ClassNode;
import org.designwizard.design.MethodNode;
import org.designwizard.design.FieldNode;
import org.designwizard.design.PackageNode;

public class DesignTest {
    @Test
    public void testFacadeDoesNotReferenceSubsystemObjects() throws Exception {
        // Always instantiate DesignWizard exactly like this
        DesignWizard dw = new DesignWizard("bin");

        // Get the Facade class
        ClassNode facadeClass = dw.getClass("com.cnblog.clarck.Facede");

        // Get the subsystem classes
        ClassNode subSystemOne = dw.getClass("com.cnblog.clarck.SubSystemOne");
        ClassNode subSystemTwo = dw.getClass("com.cnblog.clarck.SubSystemTwo");
        ClassNode subSystemThree = dw.getClass("com.cnblog.clarck.SubSystemThree");
        ClassNode subSystemFour = dw.getClass("com.cnblog.clarck.SubSystemFour");

        // Get all methods in the Facade class
        Set<MethodNode> facadeMethods = facadeClass.getAllMethods();

        // Iterate through each method in the Facade class
        for (MethodNode method : facadeMethods) {
            // Get the classes referenced by this method
            Set<ClassNode> calleeClasses = method.getCalleeClasses();

            // Assert that the method does not reference any subsystem classes directly
            assertFalse(calleeClasses.contains(subSystemOne));
            assertFalse(calleeClasses.contains(subSystemTwo));
            assertFalse(calleeClasses.contains(subSystemThree));
            assertFalse(calleeClasses.contains(subSystemFour));
        }
    }
}
