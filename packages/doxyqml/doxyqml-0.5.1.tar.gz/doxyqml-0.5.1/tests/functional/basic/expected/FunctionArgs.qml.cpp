using namespace QtQuick;
/*
 * Header bla
 */
/**
 * A very simple item
 */
class FunctionArgs : public QtQuick.Item {
public:
/**
     * The 'foo' property
     */
Q_PROPERTY(int foo READ dummyGetter_foo_ignore)

Q_SIGNALS: void clicked(int x, int y); public:

Q_SIGNALS: void activated(); public:
/**
     * Do something with arg1 and arg2
     * @param arg1 first argument
     * @param arg2 second argument
     */
void doSomething(string arg1, int arg2);
/**
     * A badly documented function. Missing one argument and documenting a
     * non-existing document
     * @param foo first argument
     * @param baz this argument does not exist
     */
void badlyDocumented(string foo, bar);

Q_PROPERTY(string escaped READ dummyGetter_escaped_ignore)

Q_PROPERTY(string block READ dummyGetter_block_ignore)
/**
     * Compute the arg^2
     * @return the result
     */
int square(arg);
/**
     * Function with int default parameter
     * @param arg A parameter with a defaultvalue
     * @return the result
     */
int intDefaultParameter(int arg = 0);
/**
     * Function with string default parameter
     * @param arg A parameter with a default value
     * @return the result
     */
string stringDefaultParameter(string arg = "hello");
/**
     * Function with property as default parameter
     * @param arg A parameter with a default value
     * @return the result
     */
int propDefaultParameter(int arg = foo);
/// One-line comment
void refresh();

Q_PROPERTY(int weirdProperty READ dummyGetter_weirdProperty_ignore)
/* baz */
/* foo */
};
